from api.structure.base import BaseView  # do not remove it
from api.structure.collect import CollectBaseView, CursorCollectBaseView
from api.structure.create import CreateBaseView
from api.structure.delete import DeleteBaseView
from api.structure.edit import EditBaseView
from api.structure.retrieve import RetrieveBaseView


class CreateView(CreateBaseView):
    """
    APIView for Create objects
    """

    def __init_subclass__(self) -> None:
        super().__init_subclass__()
        super().Validator.serializer_class(self)


class RetrieveView(RetrieveBaseView):
    """
    APIView for get object
    """

    def __init_subclass__(self) -> None:
        super().__init_subclass__()
        super().Validator.service(self)
        super().Validator.output_serializer_class(self)


class CollectView(CollectBaseView):
    """
    APIView for List objects
    """

    def __init_subclass__(self) -> None:
        super().__init_subclass__()
        super().Validator.service(self)
        super().Validator.output_serializer_class(self)


class CursorCollectView(CursorCollectBaseView):
    """
    APIView for List objects
    """

    def __init_subclass__(self) -> None:
        super().__init_subclass__()
        super().Validator.service(self)
        super().Validator.output_serializer_class(self)


class EditView(EditBaseView):
    """
    APIView for Edit objects
    """

    def __init_subclass__(self) -> None:
        super().__init_subclass__()
        super().Validator.service(self)
        super().Validator.serializer_class(self)


class DeleteView(DeleteBaseView):
    """
    APIView for Delete a object
    """

    def __init_subclass__(self) -> None:
        super().__init_subclass__()
        super().Validator.service(self)


class ListView(CollectBaseView, CreateBaseView):
    """
    APIView for Create, or List objects
    """

    def __init_subclass__(self) -> None:
        super().__init_subclass__()
        super().Validator.service(self)
        super().Validator.serializer_class(self)
        super().Validator.output_serializer_class(self)


class CursorListView(CursorCollectBaseView, CreateBaseView):
    """
    APIView for Create, or List objects (using cursor pagination)
    """

    def __init_subclass__(self) -> None:
        super().__init_subclass__()
        super().Validator.service(self)
        super().Validator.serializer_class(self)
        super().Validator.output_serializer_class(self)


class DetailView(RetrieveBaseView, EditBaseView, DeleteBaseView):
    """
    APIView for Read, Update, or Delete object
    """

    def __init_subclass__(self) -> None:
        super().__init_subclass__()
        super().Validator.service(self)
        super().Validator.serializer_class(self)
        super().Validator.output_serializer_class(self)
