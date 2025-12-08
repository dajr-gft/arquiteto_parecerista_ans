from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from fastapi import File, UploadFile, Form, HTTPException
import base64


