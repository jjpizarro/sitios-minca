from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.models.place import Place 
from app.schemas.place import PlaceCreate, PlaceUpdate

#Create, Read, Update, Delete
#Read un sólo lugar por el id, obtener todos los lugares
"""obtiene un place por el id"""
def get(db:Session, place_id:int) -> Place:
    #SQL -> select * from places where places.id = place_id
    return db.query(Place).filter(Place.id == place_id).first()

"""Obtener todos los sitios"""
def get_places(db:Session, skip: int = 0, limit: int = 10):
     #SQL -> select * from places where places.id = place_id limit 10
    return db.query(Place).offset(skip).limit(limit).all()

"""Crear un sitio"""
def create_place(db:Session, place: PlaceCreate):
     #SQL -> insert into places (name, description, image)  values ('','','',''); commit
    db_place = Place(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

"""Actualizar un sitio"""
def update_place(db:Session, *,db_obj:Place, obj_in: PlaceUpdate)-> Place:
    #SQL update places set name=? ...
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in,dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj,field, update_data[field])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

"""Eliminar un sitio"""
def delete_place (db:Session, *, id: int)->Place:
    #SQL select * from places where id = ?
    obj = db.query(Place).get(id)
     #SQL Delete from places where id = ?
    db.delete(obj)
    db.commit()
    return obj