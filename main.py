from fastapi import FastAPI
import redis

app = FastAPI()

redis_url = "redis://:4okRPRToSOjkgIlmcoQMoMorn06GuaRgMUmPq55SqC6VoWcjMvXjUeQQXz0lyOH4@194.195.254.249:5432/0"
redis_client = redis.from_url(redis_url)


@app.post("/add-task/")
def add_task(data: dict):
    # 将任务推送到 Redis 列表
    redis_client.lpush("task_queue", data["task_data"])
    return {"status": "Task added to Redis"}
