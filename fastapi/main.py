import asyncpg
import uvicorn

from fastapi import Body, FastAPI

app = FastAPI()

# Заменить на свою бд:
# DATABASE_URL = "postgresql://postgres:admin@localhost:5433/postgres"

# Прод:
DATABASE_URL = "postgresql://postgres:admin@db:5432/postgres"


async def execute_sql(query, params=None):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        print(f"Executing SQL: {query}")
        print(f"With parameters: {params}")
        if params:
            result = await conn.fetch(query, *params)
        else:
            result = await conn.fetch(query)
        return result
    finally:
        await conn.close()


@app.post("/fastapi/search_v2/part/")
async def search_parts(request_body: dict = Body(...)):
    filters = []
    query_params = []

    mark_list = request_body.get("mark_list")
    mark_name = request_body.get("mark_name")
    part_name = request_body.get("part_name")
    params = request_body.get("params", {})
    price_gte = request_body.get("price_gte")
    price_lte = request_body.get("price_lte")
    page = request_body.get("page", 1)

    param_counter = 1
    if mark_list:
        filters.append(f"m.id = ANY(${param_counter})")
        query_params.append(mark_list)
        param_counter += 1
    elif mark_name:
        filters.append(f"m.name ILIKE ${param_counter}")
        query_params.append(f"{mark_name}%")
        param_counter += 1

    if part_name:
        filters.append(f"p.name ILIKE ${param_counter}")
        query_params.append(f"%{part_name.capitalize()}%")
        param_counter += 1

    if params:
        for key, value in params.items():
            if value is not None:
                if isinstance(value, bool):
                    value_str = "true" if value else "false"
                else:
                    value_str = str(value)
                filters.append(f"p.json_data->>'{key}' = ${param_counter}")
                query_params.append(value_str)
                param_counter += 1

    if price_gte is not None:
        filters.append(f"price >= ${param_counter}")
        query_params.append(price_gte)
        param_counter += 1

    if price_lte is not None:
        filters.append(f"price <= ${param_counter}")
        query_params.append(price_lte)
        param_counter += 1

    base_query = """
    SELECT m.id AS mark_id,
    m.name AS mark_name,
    m.producer_country_name AS producer_country_name,
    md.id AS model_id, md.name AS model_name,
    p.name AS part_name, p.json_data AS json_data, p.price AS price
    FROM autoparts_part p
    INNER JOIN autoparts_model md ON p.model_id = md.id
    INNER JOIN autoparts_mark m ON md.mark_id = m.id
"""

    if filters:
        where_clause = "WHERE " + " AND ".join(filters)
        base_query += where_clause

    count_query = """
    SELECT COUNT(*) AS total_count
    FROM autoparts_part p
    INNER JOIN autoparts_model md ON p.model_id = md.id
    INNER JOIN autoparts_mark m ON md.mark_id = m.id
"""
    count_query += where_clause

    sum_query = """
    SELECT COALESCE(SUM(p.price), 0) AS total_sum
    FROM autoparts_part p
    INNER JOIN autoparts_model md ON p.model_id = md.id
    INNER JOIN autoparts_mark m ON md.mark_id = m.id
"""
    sum_query += where_clause

    total_count = await execute_sql(count_query, query_params)
    total_sum = await execute_sql(sum_query, query_params)

    total_count = total_count[0]["total_count"]
    total_sum = total_sum[0]["total_sum"]

    limit = 10
    offset = (page - 1) * limit
    query = base_query + f" ORDER BY p.id OFFSET {offset} LIMIT {limit}"

    results = await execute_sql(query, query_params)

    response_data = {
        "response": results,
        "count": total_count,
        "summ": total_sum,
        "page": page,
    }

    return response_data


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
