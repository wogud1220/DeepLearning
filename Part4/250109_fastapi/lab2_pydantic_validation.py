from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="Pydantic 데이터 검증 실습")

# ============================================
# 1단계: 기본 Pydantic 모델
# ============================================

# 클라가 보내야할 형식 모델
class UserCreate(BaseModel):
    """사용자 생성 요청 모델"""
    username : str
    email: str
    age: int

    # 예시 데이터 (Swagger UI에서 자동으로 표시됨)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "홍길동",
                    "email": "hong@example.com",
                    "age": 25
                }
            ]
        }   
    }


# 서버가 클라에게 줘야할 형태
class UserResponse(BaseModel):
    """사용자 응답 모델"""
    id: int
    username: str
    email: str
    age: int
    created_at: str

# 간단한 인메모리 저장소
fake_db = []
user_id_counter = 1


# response_model “이 API가 최종적으로 사용자에게 돌려주는 응답의 형태(스키마)를 지정한다”
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    """
    사용자 생성 API
    💡 Pydantic이 자동으로 해주는 것:
    1. JSON → Python 객체 변환
    2. 타입 검증 (age에 문자열 넣으면 에러!)
    3. 필수 필드 확인
    """
    global user_id_counter

    new_user = {
        "id": user_id_counter,
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "created_at": datetime.now().isoformat()
    }
    fake_db.append(new_user)
    user_id_counter += 1

    return new_user

@app.get("/users", response_model=List[UserResponse])
def get_users():
    """저장된 사용자 목록 조회"""
    return fake_db



# ============================================
# 2단계: 필드 검증 (Field Validation)
# ============================================
# 입력을 이런 식으로 받을거다.
class ProductCreate(BaseModel):
    """상품 등록 모델 - 필드 검증 포함"""
    
    name: str = Field(
        min_length=2,           # 최소 2글자
        max_length=100,         # 최대 100글자
        description="상품명"
    )
    
    price: int = Field(
        gt=0,                   # 0보다 커야 함 (greater than)
        le=10000000,            # 1000만원 이하 (less than or equal)
        description="가격 (원)"
    )
    
    quantity: int = Field(
        ge=0,                   # 0 이상 (greater than or equal)
        default=0,
        description="재고 수량"
    )
    
    category: str = Field(
        pattern=r"^(전자제품|의류|식품|기타)$",  # 정규식 패턴
        description="카테고리"
    )
    
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="상품 설명 (선택)"
    )

# 상품 저장소
products_db = []
product_id_counter = 1


@app.post("/products")
def create_product(product: ProductCreate):
    """
    상품 등록 API
    
    테스트해보기:
    - price에 -100 입력 → 에러!
    - name에 "A" 한 글자 입력 → 에러!
    - category에 "가구" 입력 → 에러!
    """
    global product_id_counter

    new_product = {
        "id": product_id_counter,
        **product.model_dump(),                    # Pydantic 모델을 python dict로 바꿔서, 응답 dict에 그대로 합침
        "created_at": datetime.now().isoformat()
    }
    products_db.append(new_product)
    product_id_counter += 1

    return {
        "message": "상품 등록 성공",
        "product": new_product
    }

@app.get("/products")
def get_products():
    """상품 목록 조회"""
    return {"products": products_db, "total": len(products_db)}


# ============================================
# 3단계: 커스텀 Validator
# ============================================
class ChatMessage(BaseModel):
    """채팅 메시지 모델  - 커스텀 검증"""

    role: str = Field(description="메시지 역할")
    content: str = Field(min_length=1, description="메시지 내용")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        """role은 user, assistant, system 중 하나여야 함"""
        allowed_roles = ['user','assistant','system']
        if v not in allowed_roles:
            raise ValueError(f"role은 {allowed_roles} 중 하나여야 합니다.")
        return v

class ChatRequest(BaseModel):
    """채팅 요청 모델"""
    messages: List[ChatMessage] = Field(
        min_length=1,
        description="대화 메시지 목록"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="창의성 조절(0~2)"
    )
    max_tokens: int = Field(
        default=1000,
        ge=1,
        le=4096,
        description="최대 생성 토큰 수"
    )

    # 예시 데이터 (Swagger UI에서 자동으로 표시됨)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [
                        {"role": "system", "content":"당신은 친절한 AI 어시스턴트입니다."},
                        {"role": "user", "content":"안녕하세요!"}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            ]
        }
    }

@app.post("/chat")
def chat(request: ChatRequest):
    """
    채팅 API(모델 연동 전 구조만)

    !!! 실제 LLM 연동 전에 API 구조를 먼저 설계하는 것이 좋습니다 !!!
    """
    return {
        "message": "채팅 요청 접수",
        "received": {
            "message_count": len(request.messages),
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "last_message": request.messages[-1].content
        }
    }


# ============================================
# 4단계: 응답 모델로 필터링
# ============================================
class UserInternal(BaseModel):
    """내부용 사용자 모델(민감정보 포함)"""
    id: int
    username: str
    email: str
    password_hash: str      # 민감정보!
    is_admin: bool

class UserPublic(BaseModel):
    """외부 노출용 사용자 모델"""
    id: int
    username: str
    # email, password_hash, is_admin은 노출하지 않음

# 가짜 유저 데이터(테스트용)
internal_users = [
    UserInternal(
        id=1, 
        username="admin", 
        email="admin@test.com",
        password_hash="hashed_secret_123",
        is_admin=True
    ),
    UserInternal(
        id=2,
        username="user1",
        email="user1@test.com",
        password_hash="hashed_password_456",
        is_admin=False
    )
]

@app.get("/users/{user_id}/public", response_model=UserPublic)
def get_user_public(user_id: int):
    """
    사용자 공개 정보 조회
    
    !!! response_model을 지정하면 해당 필드만 응답에 포함! - 민감정보가 실수로 노출되는 것을 방지합니다.
    """
    for user in internal_users:
        if user.id == user_id:
            return user
        
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")


@app.get("/users/{user_id}/internal", response_model=UserInternal)
def get_user_internal(user_id: int):
    """
    사용자 내부 정보 조회 (관리자용 - 실제로는 인증 필요!!!)
    """
    for user in internal_users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")



"""
[혼자해보기 2-1] BookCreate 모델 만들기:
- title: str (2~200자)
- author: str (필수)
- isbn: str (정확히 13자리 숫자) - 힌트: pattern=r"^[0-9]{13}$"
- price: int (1000원 이상, 100만원 이하)
- published_year: int (1900~2025)
- genre: str ("소설", "비문학", "자기계발", "기술" 중 하나)
"""

class BookCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )
    author: str
    isbn: str = Field(
        pattern=r"^[0-9]{13}$",
    )
    price: int = Field(
        ge=1000,
        le=1_000_000
    )
    published_year: int = Field(
        ge=1900,
        le=2025
    )
    genre: str = Field(
        pattern=r"^(소설|비문학|자기계발|기술)$"
    )

"""
[혼자해보기 2-2] POST /books 엔드포인트 만들기:
- BookCreate를 받아서 저장
- BookResponse 모델로 응답 (id, created_at 추가)
"""


class BookRepository:
    books = []
    id = 1

    @classmethod
    def create(cls, book_data: dict) -> dict:

        for book in cls.books:
            if book["title"] == book_data["title"]:
                raise HTTPException(
                    status_code=400,
                    detail="이미 존재하는 책 제목입니다."
                )

        new_book = {
            "id": cls.id,
            **book_data,
            "created_at": datetime.now()
        }
        cls.books.append(new_book)
        cls.id += 1
        return new_book

    @classmethod
    def get_all(cls):
        return cls.books

    @classmethod
    def get_by_title(cls, title: str):
        for book in cls.books:
            if book["title"] == title:
                return book
            else:
                raise HTTPException(
                    status_code=400,
                    detail="없는 책입니다."
                )

class BookCreatedResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    price: int
    published_year: int
    genre: str
    created_at: datetime



@app.post("/books", response_model=BookCreatedResponse)
def create_books(book: BookCreate):
    new_book = BookRepository.create(book.model_dump())
    return new_book


@app.get("/books", response_model=List[BookCreatedResponse])
def get_books():
    return BookRepository.get_all()

@app.get("/book", response_model=BookCreatedResponse)
def get_book(book_title: str):
    return BookRepository.get_by_title(book_title)
