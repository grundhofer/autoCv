"""Pydantic models for structured CV data."""

from typing import List, Optional

from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    """Basic personal / contact information."""

    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    job_title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    availability: Optional[str] = None


class WorkExperience(BaseModel):
    """A single work-experience entry."""

    job_title: str
    company: Optional[str] = None
    client: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)


class Education(BaseModel):
    """A single education entry."""

    degree: str
    institution: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    details: Optional[str] = None


class SkillCategory(BaseModel):
    """A group of related skills."""

    category: str
    skills: List[str] = Field(default_factory=list)


class Certification(BaseModel):
    """A professional certification or course."""

    name: str
    issuer: Optional[str] = None
    date: Optional[str] = None


class Language(BaseModel):
    """A spoken / written language with proficiency."""

    language: str
    proficiency: Optional[str] = None


class Project(BaseModel):
    """A notable project (if listed separately from work experience)."""

    name: str
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CVData(BaseModel):
    """Root schema for all extracted CV data."""

    personal_info: PersonalInfo
    summary: Optional[str] = None
    experience: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    skills: List[SkillCategory] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    languages: List[Language] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
