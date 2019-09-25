def decide_on_model(model):
        """Small helper function to pipe all DB operations of a worlddata model to the world_data DB"""
        return 'Crime' if model._meta.app_label == 'Crime' else None


class CrimeDbRouter:
    def db_for_read(self, model, **hints):
        return decide_on_model(model)

    def db_for_write(self, model, **hints):
        return decide_on_model(model)

    def allow_relation(self, obj1, obj2, **hints):
        # Allow any relation if both models are part of the worlddata app
        if obj1._meta.app_label == 'crimedata' and obj2._meta.app_label == 'crimedata':
            return True
        # Allow if neither is part of worlddata app
        elif 'crimedata' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        # by default return None - "undecided"
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'default' and app_label != "crimedata":
            return True
        if db == "crime_data" and app_label == "crimedata":
            return True
        return False

