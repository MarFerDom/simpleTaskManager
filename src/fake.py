from typing import Iterator, Optional, Tuple, List, Any

fake_answer = False

class BaseFakeModel():
    def get_all_tasks(self,
                      user: Optional[str] = None) -> Tuple[List[str], List[int]]:
        ...
    def get_task(self, index: int) -> Any:
        ...
    def mark_as_completed(self, task_id:int) -> None:
        ...
    def save_tasks(self):
        ...
    def read_report(self, userlist: List[str]) -> str:
        ...
    def write_report(self, userlist: List[str]) -> None:
        ...

class FakeModel(BaseFakeModel):
    def add_task(self, data: List[str]) -> bool:
        return fake_answer
    def edit_user(self, task_id:int, owner:str) -> bool:
        return fake_answer
    def edit_date(self, task_id:int, date:str) -> bool:
        return fake_answer
    
class BaseFakeUser():
    def user_exists(self, user:str, *args, **kwargs) -> bool:
        ...
    @property
    def user_logged(self) -> Optional[str]:
        ...  
    @property
    def is_admin(self) -> bool:
        ...
    @property
    def users(self) -> Iterator[str]:
        ...
    def __len__(self) -> int:
        ...

class FakeUser(BaseFakeUser):
    def add_user(self, user:str, pwd:str) -> bool:
        return fake_answer
    def log_in(self, user:str, pwd:str) -> bool:
        return fake_answer