import uuid


class UUIDProvider:
    @staticmethod
    def generate_id() -> str:
        return str(uuid.uuid4())