import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';
import styled from 'styled-components';
import Column from './Column';
import AddColumn from './AddColumn';

const Container = styled.div`
  display: flex;
`;

function Board(props) {
    const initialData = {tasks: {}, columns: {}, columnOrder: []};
    const [state, setState] = useState(initialData);

    useEffect(() => {
        fetchBoard().then(board => setState(board));
    }, [props.token]);

    useEffect(() => {
        if (state !== initialData) {
            saveBoard();
        }
    }, [state]);

    async function saveBoard() {
        const response = await fetch("/board", {
            method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization" : "Bearer " + props.token
                },
            body: JSON.stringify(state)
        });
        const data = await response.json();
    }

    async function fetchBoard() {
        const response = await fetch('/board', {headers: {"Authorization" : "Bearer " + props.token}});
        const data = await response.json();
        return data.board;
    }

    function onDragEnd(result) {
        const { destination, source, draggableId, type } = result;

        if (!destination) {
            return;
        }
        
        if (destination.droppableId === source.droppableId && destination.index === source.index) {
            return;
        }

        if (type === 'column') {
            const newColumnOrder = Array.from(state.columnOrder);
            newColumnOrder.splice(source.index, 1);
            newColumnOrder.splice(destination.index, 0, draggableId);
      
            setState({
                ...state,
                columnOrder: newColumnOrder,
            });
            return;
        }

        const start = state.columns[source.droppableId]; 
        const finish = state.columns[destination.droppableId]; 

        if (start === finish) {
            const newTaskIds = Array.from(start.taskIds);
            newTaskIds.splice(source.index, 1);
            newTaskIds.splice(destination.index, 0, draggableId);
      
            const newColumn = {
                ...start,
                taskIds: newTaskIds,
            }
      
            setState({...state, 
                columns: {
                ...state.columns,
                [newColumn.id]: newColumn}
            });
            return;
        }

        const startTaskIds = Array.from(start.taskIds);
        startTaskIds.splice(source.index, 1);
        const newStart = {
            ...start,
            taskIds: startTaskIds,
        }
    
        const finishTaskIds = Array.from(finish.taskIds);
        finishTaskIds.splice(destination.index, 0, draggableId);
        const newFinish = {
            ...finish,
            taskIds: finishTaskIds,
        }
    
        setState({...state, 
            columns: {
                ...state.columns,
                [newStart.id]: newStart,
                [newFinish.id]: newFinish,
            }
        });
    }

    return (
        <DragDropContext onDragEnd={onDragEnd}>
            <AddColumn state={state} setState={setState} />
            <Droppable droppableId="all-columns" direction="horizontal" type="column">
                {provided => (
                    <Container {...provided.droppableProps} ref={provided.innerRef}>
                        {
                            state.columnOrder.map((columnId, index) => {
                                const column = state.columns[columnId];
                                const tasks = column.taskIds.map(taskId => state.tasks[taskId]);
                                return <Column key={column.id} column={column} tasks={tasks} index={index} state={state} setState={setState} />;
                            })
                        }
                        {provided.placeholder}
                    </Container>
                )}
            </Droppable>
        </DragDropContext>
    )
}

export default Board;