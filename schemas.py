"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Public-facing inquiry submitted from the website contact form
class Inquiry(BaseModel):
    name: str = Field(..., description="Nom complet du client")
    email: Optional[EmailStr] = Field(None, description="Adresse email")
    phone: Optional[str] = Field(None, description="Numéro de téléphone")
    service: Optional[str] = Field(None, description="Service demandé (ex: Débouchage, Fuite)")
    zone: Optional[str] = Field(None, description="Zone d'intervention")
    message: str = Field(..., description="Message du client")
    source: Optional[str] = Field("website", description="Source du lead (website, whatsapp, call)")
    consent: bool = Field(True, description="Consentement pour être contacté")

# Example schemas (you can extend as needed)
class User(BaseModel):
    name: str
    email: EmailStr
    address: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category: str
    in_stock: bool = True
