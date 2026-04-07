from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, String, Text, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase):
    pass


class Breeder(Base):
    __tablename__ = "breeders"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    breeder_id: Mapped[int] = mapped_column(ForeignKey("breeders.id"))
    name: Mapped[str] = mapped_column(String(120))
    objective: Mapped[Optional[str]] = mapped_column(Text, default=None)
    visibility: Mapped[str] = mapped_column(String(20), default="private")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    breeder: Mapped[Breeder] = relationship()


class Genetic(Base):
    __tablename__ = "genetics"
    id: Mapped[int] = mapped_column(primary_key=True)
    canonical_name: Mapped[str] = mapped_column(String(120), unique=True)
    breeder_id: Mapped[Optional[int]] = mapped_column(ForeignKey("breeders.id"), default=None)
    generation: Mapped[Optional[str]] = mapped_column(String(20), default=None)
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    visibility: Mapped[str] = mapped_column(String(20), default="public")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    breeder: Mapped[Optional[Breeder]] = relationship()


class GeneticRelationship(Base):
    __tablename__ = "genetic_relationships"
    id: Mapped[int] = mapped_column(primary_key=True)
    from_genetic_id: Mapped[int] = mapped_column(ForeignKey("genetics.id"))
    to_genetic_id: Mapped[int] = mapped_column(ForeignKey("genetics.id"))
    relation_type: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Cross(Base):
    __tablename__ = "crosses"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    mother_genetic_id: Mapped[int] = mapped_column(ForeignKey("genetics.id"))
    father_genetic_id: Mapped[int] = mapped_column(ForeignKey("genetics.id"))
    resulting_genetic_id: Mapped[Optional[int]] = mapped_column(ForeignKey("genetics.id"), default=None)
    generation_expected: Mapped[Optional[str]] = mapped_column(String(20), default=None)
    objective: Mapped[Optional[str]] = mapped_column(Text, default=None)
    visibility: Mapped[str] = mapped_column(String(20), default="private")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class PhenotypeBatch(Base):
    __tablename__ = "phenotype_batches"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    cross_id: Mapped[Optional[int]] = mapped_column(ForeignKey("crosses.id"), default=None)
    name: Mapped[str] = mapped_column(String(120))
    visibility: Mapped[str] = mapped_column(String(20), default="private")


class Phenotype(Base):
    __tablename__ = "phenotypes"
    id: Mapped[int] = mapped_column(primary_key=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey("phenotype_batches.id"))
    code: Mapped[str] = mapped_column(String(50))
    aroma_score: Mapped[Optional[float]] = mapped_column(default=None)
    resin_score: Mapped[Optional[float]] = mapped_column(default=None)
    vigor_score: Mapped[Optional[float]] = mapped_column(default=None)
    decision: Mapped[str] = mapped_column(String(20), default="pending")


class Observation(Base):
    __tablename__ = "observations"
    id: Mapped[int] = mapped_column(primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(30))
    entity_id: Mapped[int] = mapped_column()
    note: Mapped[str] = mapped_column(Text)
    visibility: Mapped[str] = mapped_column(String(20), default="private")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class BreederCreate(BaseModel):
    name: str
    slug: str
    bio: Optional[str] = None


class GeneticCreate(BaseModel):
    canonical_name: str
    breeder_id: Optional[int] = None
    generation: Optional[str] = None
    description: Optional[str] = None
    visibility: str = "public"


class RelationshipCreate(BaseModel):
    from_genetic_id: int
    to_genetic_id: int
    relation_type: str


class ProjectCreate(BaseModel):
    breeder_id: int
    name: str
    objective: Optional[str] = None
    visibility: str = "private"


class CrossCreate(BaseModel):
    project_id: int
    mother_genetic_id: int
    father_genetic_id: int
    resulting_genetic_id: Optional[int] = None
    generation_expected: Optional[str] = None
    objective: Optional[str] = None


class BatchCreate(BaseModel):
    project_id: int
    cross_id: Optional[int] = None
    name: str


class PhenotypeCreate(BaseModel):
    batch_id: int
    code: str
    aroma_score: Optional[float] = None
    resin_score: Optional[float] = None
    vigor_score: Optional[float] = None
    decision: str = "pending"


class ObservationCreate(BaseModel):
    entity_type: str
    entity_id: int
    note: str
    visibility: str = "private"


engine = create_engine("sqlite:///./breeders.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="Breeders Genetics Platform MVP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/breeders")
def create_breeder(payload: BreederCreate):
    with SessionLocal() as db:
        breeder = Breeder(**payload.model_dump())
        db.add(breeder)
        db.commit()
        db.refresh(breeder)
        return breeder


@app.get("/api/breeders")
def list_breeders():
    with SessionLocal() as db:
        return db.query(Breeder).order_by(Breeder.name.asc()).all()


@app.post("/api/genetics")
def create_genetic(payload: GeneticCreate):
    with SessionLocal() as db:
        genetic = Genetic(**payload.model_dump())
        db.add(genetic)
        db.commit()
        db.refresh(genetic)
        return genetic


@app.get("/api/genetics")
def list_genetics(q: Optional[str] = None):
    with SessionLocal() as db:
        query = db.query(Genetic)
        if q:
            query = query.filter(Genetic.canonical_name.ilike(f"%{q}%"))
        return query.order_by(Genetic.canonical_name.asc()).all()


@app.get("/api/genetics/{genetic_id}")
def get_genetic(genetic_id: int):
    with SessionLocal() as db:
        genetic = db.get(Genetic, genetic_id)
        if not genetic:
            raise HTTPException(status_code=404, detail="Genetic not found")
        return genetic


@app.post("/api/relationships")
def create_relationship(payload: RelationshipCreate):
    with SessionLocal() as db:
        relationship = GeneticRelationship(**payload.model_dump())
        db.add(relationship)
        db.commit()
        db.refresh(relationship)
        return relationship


@app.get("/api/genetics/{genetic_id}/tree")
def genetic_tree(genetic_id: int):
    with SessionLocal() as db:
        center = db.get(Genetic, genetic_id)
        if not center:
            raise HTTPException(status_code=404, detail="Genetic not found")

        rels = db.query(GeneticRelationship).all()
        ids = {genetic_id}
        for rel in rels:
            if rel.from_genetic_id == genetic_id or rel.to_genetic_id == genetic_id:
                ids.add(rel.from_genetic_id)
                ids.add(rel.to_genetic_id)
        nodes = db.query(Genetic).filter(Genetic.id.in_(ids)).all()

        return {
            "center": center.id,
            "nodes": [{"id": n.id, "label": n.canonical_name} for n in nodes],
            "edges": [
                {
                    "id": r.id,
                    "source": r.from_genetic_id,
                    "target": r.to_genetic_id,
                    "relation_type": r.relation_type,
                }
                for r in rels
                if r.from_genetic_id in ids and r.to_genetic_id in ids
            ],
        }


@app.post("/api/projects")
def create_project(payload: ProjectCreate):
    with SessionLocal() as db:
        project = Project(**payload.model_dump())
        db.add(project)
        db.commit()
        db.refresh(project)
        return project


@app.get("/api/projects")
def list_projects():
    with SessionLocal() as db:
        return db.query(Project).order_by(Project.created_at.desc()).all()


@app.post("/api/crosses")
def create_cross(payload: CrossCreate):
    with SessionLocal() as db:
        cross = Cross(**payload.model_dump())
        db.add(cross)
        db.commit()
        db.refresh(cross)
        return cross


@app.get("/api/projects/{project_id}/crosses")
def list_project_crosses(project_id: int):
    with SessionLocal() as db:
        return db.query(Cross).filter(Cross.project_id == project_id).all()


@app.post("/api/batches")
def create_batch(payload: BatchCreate):
    with SessionLocal() as db:
        batch = PhenotypeBatch(**payload.model_dump())
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch


@app.get("/api/batches/{batch_id}/phenotypes")
def list_phenotypes(batch_id: int):
    with SessionLocal() as db:
        return db.query(Phenotype).filter(Phenotype.batch_id == batch_id).all()


@app.post("/api/phenotypes")
def create_phenotype(payload: PhenotypeCreate):
    with SessionLocal() as db:
        pheno = Phenotype(**payload.model_dump())
        db.add(pheno)
        db.commit()
        db.refresh(pheno)
        return pheno


@app.post("/api/observations")
def create_observation(payload: ObservationCreate):
    with SessionLocal() as db:
        obs = Observation(**payload.model_dump())
        db.add(obs)
        db.commit()
        db.refresh(obs)
        return obs


@app.get("/api/observations/{entity_type}/{entity_id}")
def list_observations(entity_type: str, entity_id: int):
    with SessionLocal() as db:
        return (
            db.query(Observation)
            .filter(Observation.entity_type == entity_type, Observation.entity_id == entity_id)
            .order_by(Observation.created_at.desc())
            .all()
        )


app.mount("/", StaticFiles(directory="external_projects/cannabis_breeders_platform/breeders_app/frontend", html=True), name="frontend")
