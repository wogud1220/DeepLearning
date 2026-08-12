from fastapi import FastAPI

app = FastAPI(
    title="첫번째 FastAPI",
    description="AI 엔지니어 FastAPI 실습 1",
    version="1.0.0"
)

@app.get("/")
def home():
    """루트 경로: 서버가 잘 동작하는지 확인"""
    return {"message": "FastAPI server!"}

@app.get("/health")
def health_check():
    """헬스체크 - 서버 상태 확인용 (실무에서 필수!)"""
    return {"status": "healthy"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "message": f"{user_id}번 사용자 정보입니다"
    }

@app.get("/items/{item_name}")
def get_item(item_name: str):
    return {
        "item_name": item_name,
        "message": f"'{item_name}' 아이템을 조회합니다."
    }

# ============================================
# 3단계: 쿼리 매개변수 (Query Parameter)
# URL 뒤에 ?key=value 형태로 전달
# ============================================
@app.get("/search")
def search_items(
    keyword: str,           # 필수 파라미터
    skip,
    limit: int = 10,        # 선택 파라미터 (기본값: 10)
         # 선택 파라미터 (기본값: 0)
):
    """
    쿼리 매개변수 예시
    - /search?keyword=AI → keyword="AI", limit=10, skip=0
    """
    return {
        "keyword": keyword,
        "limit": limit,
        "skip": skip,
        "message": f"{keyword}로 검색, {skip}번째부터 {limit}개 조회"
    }

# ============================================
# 4단계: 경로 + 쿼리 매개변수 조합
# ============================================
@app.get("/categories/{category}/products")
def get_products_by_category(
    category: str,          # 경로 매개변수
    min_price: int = 0,     # 쿼리 매개변수
    max_price: int = 100000,
    sort_by: str = "name"
):
    """
    실전 예시: 카테고리별 상품 조회
    - /categories/electronics/products?min_price=1000&sort_by=price
    """
    return {
        "category": category,
        "filters": {
            "min_price": min_price,
            "max_price": max_price,
            "sort_by": sort_by
        },
        "message": f"{category} 카테고리 상품 조회"
    }


# 1. GET /greeting/{name}
#    - 경로로 이름을 받아서 "안녕하세요, {name}님!" 반환


#Path
@app.get('/greeting/{name}')
def get_greeting(name: str):
    return f"hi, {name}! "

# query
@app.get('/greeting')
def get_greeting_2(name: str):
    return f"hello, {name}!"


# 2. GET /calculate
#    - 쿼리 파라미터: a (int), b (int), operation (str, 기본값="add")
#    - operation이 "add"면 a+b, "multiply"면 a*b 반환
@app.get('/calculate')
def calculate(a: int, b: int, operator: str = "add"):
    return a+b if operator == "add" else a*b


# 3. GET /movies/{genre}/list
#    - 경로: genre (str)
#    - 쿼리: year (int, 선택), rating (float, 기본값=0.0)
#    - 필터 조건과 함께 메시지 반환


@app.get('/movies/{genre}/list')
def get_movies(genre: str, year: int = 2026, rating: float = 0.0):

    return {
        "genre": genre,
        "year": year,
        "rating": rating,
        "message": f"{genre} search results"
    }




