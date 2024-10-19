# AT_EDUCATION

Микросервис оценки обучаемого АТ-ТЕХНОЛОГИЯ

#

![scheme](education.svg)

Обучаемый в Компоненте-Х выполняет некоторые действия. В ответ на эти действия очередь сообщений отправляются события. Нужно определить:

1. Набор действий пользователя, в ответ на которые будут отправляться события.
2. Как описать событие? (нужна структура данных).

В подсистеме оценки навыков/умений необходимо определить схемы данных:

1. Как представить задания в БД.
2. Как представить навыки в БД.
3. Как представить реакции в БД.

Через очередь сообщений события передаются в приемник событий. Из него данные попадают в соответствующий обработчик. В логике нужно будет написать как обрабатывать события:

1. Посмотреть к какому заданию относится событие.
2. Посмотреть с каким навыком связано данное событие. 
3. Посмотреть с какой реакцией связано данное событие.
4. Отправить реакцию.

Базу данных нужно наполнить:
1. Какие навыки будут.
2. Какие задания будут.
3. Какие реакции будут.


## Модель даннных 

Входными данными являются события, которые приходят от системы Имитационного моделирования / Редактора базы знаний:

```
Event
    operation_type: CREATE | UPDATE | DELETE | GET | TRANSLATE | IMPORT | EXPORT | COMPUTE
    operand: NIL | MODEL | RESOURCE_TYPE | RESOURCE | FUNCTION | TEMPLATE | TEMPLATE_USAGE + объекты из редактора БЗ
    params: JSON
    status: SUCCESS | ERROR
    error_code: int
    error_message: str
    is_scenario: bool
```

Логика верхнего уровня:

```python

class EventManager: 
    TaskManager

    def process_event(self, event: Event):
        event_name = self.get_event_name(event)
        tasks = TaskManager.get_tasks(event_name)

        EventProcessingResults = []
        for task in task:
            EventProcessingResults.Append(TaskManager.process_event(task, event))

        return EventProcessingResults

class TaskManager:
    def get_tasks(self, event_name):
        pass

    def get_scenarios(self, task):
        pass

    def process_event(self, task, event) -> Result, Reaction:
        if event.status == "error":
            reacion = get_reaction(task, event)
        
        if event.is_scenario == true:
            self.update_scenarios(task, event)

        self.update_skills(taskm event)

```

Как будем описывать задания:

```
Task:
    id: int
    event_name: str
    event_params: NIL | JSON
    on_success: int
    on_failure: int
    skills_ids: [int] 
```

```
Scenario:
    scenario_name: str
    task_id:int
    parent_id: [int]
    dependencies: [int]
    status: TODO | DONE | IN_PROGRESS  
```


```
Skill:
    id: int
    name: str
    scenario_id: NIL | int
    tasks_ids: [int]
    scenario_name: NIL | str 
```

```
Reaction:
    id: int
    task_id: int
    message: str
```