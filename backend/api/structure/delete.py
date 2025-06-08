from api.structure import BaseView
from django.db.models.base import ModelBase
from rest_framework.response import Response


class DeleteBaseView(BaseView):
    """
    A base view for deleting model instances.

    This view handles DELETE requests to remove instances of a specified model based on filter criteria.
    It utilizes a service method to perform the deletion.

    Attributes:
        service (object): The service object containing the delete method to handle the instance deletion.
    """

    def delete(
        self,
        model: ModelBase,
        filter_kwargs: dict,
        service_method: str = "delete",
    ) -> Response:
        """
        Handles DELETE requests to remove model instances.

        This method calls the specified service method to delete instances of the provided model that match
        the filter criteria.

        Args:
            model (Type[Model]): The model class of the instances to delete.
            filter_kwargs (dict): The filter criteria to identify the instances to delete.
            service_method (str): The name of the service method to call for deletion. Defaults to "delete".

        Returns:
            Response: A DRF response with status 204 No Content.
        """

        func = getattr(self.service, service_method)
        func(model=model, filter_kwargs=filter_kwargs)
        return self.no_content()
