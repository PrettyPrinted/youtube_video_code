import React, { useState } from 'react';

function AddTask(props) {
    const [showNewTaskButton, setShowNewTaskButton] = useState(true);
    const [value, setValue] = useState("");

    function onNewTaskButtonClick() {
        setShowNewTaskButton(false);
    }

    function handleInputChange(event) {
        setValue(event.target.value);
    }

    function onNewTaskInputComplete() {
        setShowNewTaskButton(true);
        addNewTask(props.columnId, value);
        setValue("");
    }

    function addNewTask(columnId, content) {
        const newTaskId = 'task-' + Math.floor(Math.random() * 100000);
    
        const column = props.state.columns[columnId];
        const newTaskIds = Array.from(column.taskIds);
        newTaskIds.push(newTaskId);
    
        const newTask = {
            id: newTaskId,
            content: content,
        }
    
        props.setState({...props.state,
            tasks: {
                ...props.state.tasks,
                [newTaskId]: newTask
            },
            columns: {
                ...props.state.columns,
                [columnId]: {
                    ...props.state.columns[columnId],
                    taskIds: newTaskIds
                }
            }
        });
    }

    return (
        <div>
            {
                showNewTaskButton ?
                <button onClick={onNewTaskButtonClick}>New</button>:
                <input type="text" value={value} onChange={handleInputChange} onBlur={onNewTaskInputComplete} />
            }
        </div>
    )
}

export default AddTask;