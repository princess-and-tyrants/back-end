from pydantic import BaseModel

class UpdateUserReq(BaseModel):
    nickname: str | None
    mbti_ei_score : int | None
    mbti_sn_score : int | None
    mbti_tf_score : int | None
    mbti_pj_score : int | None