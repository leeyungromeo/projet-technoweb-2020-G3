"""class for static methods around the Favorite table"""

from app.repositories.recipes import RecipeRepository
from app.repositories.users import UserRepository
from app import db

from app.models.favorite import Favorite

from typing import List


class FavoriteRepository:

    @staticmethod
    def get_favorites_from(userid: int) -> List[Favorite]:
        """
        Returns all favorites from a user, or None
        """
        return Favorite.query.filter_by(user_id=userid)

    @staticmethod
    def get_favorites_to(recipeid: int) -> List[Favorite]:
        """
        Returns a list of favorites to that recipe id, or None
        """
        return Favorite.query.filter_by(recipe_id=recipeid)
    
    @staticmethod
    def get_specific_favorite(userid: int, recipeid:int) -> Favorite:
        """
        Return the specified favorite instance, or None
        """
        return Favorite.query.filter_by(user_id=userid, recipe_id=recipeid).first()


    @staticmethod
    def add_favorite(userid: int, recipeid:int) -> Favorite:
        """
        Adds a favorite to the table, provided it is valid
        if one of the targets doesn't exist

        Returns: the created favorite
        """
        #no double favorite
        if FavoriteRepository.get_specific_favorite(userid,recipeid) is not None:
            raise ValueError(f"Favorite from user {userid} to recipe {recipeid} already exists")

        user = UserRepository.find_user_by_id(userid)
        recipe = RecipeRepository.get_recipe_from_id(recipeid)

        #check that they exist
        if user is None:
            raise ValueError(f"User did not exist, ID: {userid}")
        if recipe is None:
            raise ValueError(f"Recipe did not exist, ID: {recipeid}")


        new_fav = Favorite(userid, recipeid)

        db.session.add(new_fav)

        db.session.commit()

        return new_fav



    @staticmethod
    def remove_favorite(fav_id: int) -> None:
        """Removes a subscription with some id from the database
        """

        fav = Favorite.query.get(fav_id)

        if fav is None:
            print("WARNING: Tried to remove a non-existant favorite")
            return
        
        db.session.delete(fav)
        db.session.commit()