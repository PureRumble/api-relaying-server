from locust import HttpUser, task, between

class APIUser(HttpUser):
  @task
  def visit_api(self):
    self.client.get("/")
