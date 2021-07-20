import delve.models
allmodels = dict([(name.lower(), cls) for name, cls in delve.models.__dict__.items() if isinstance(cls, type)])
class MyDBRouter(object):

    def allow_migrate(self, db, app_label, model_name = None, **hints):
        """ migrate to appropriate database per model """
        try:
            if app_label in ('sites', 'contenttypes', 'auth'):
                return True

            model = allmodels.get(model_name)
            return(model.params.db == db)
        except:
            pass


    