class TeleconsultService:
    def create_room(self, consult_id: str) -> dict:
        return {"room_id": f"room-{consult_id}", "webrtc": {"server": "stub"}}


_global_teleconsult_service: TeleconsultService | None = None


def get_teleconsult_service() -> TeleconsultService:
    global _global_teleconsult_service
    if _global_teleconsult_service is None:
        _global_teleconsult_service = TeleconsultService()
    return _global_teleconsult_service

