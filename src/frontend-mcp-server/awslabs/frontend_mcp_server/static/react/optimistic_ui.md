# Optimistic UI in React 19

Optimistic UI is a pattern that makes your React applications feel faster and more responsive by immediately updating the UI before server operations complete.

## What is Optimistic UI?

Optimistic UI is a technique where you update the user interface immediately after a user action, assuming the server request will succeed, instead of waiting for the server's response. This creates a perception of speed and responsiveness.

Examples where optimistic UI is commonly used:

- Like/comment systems in social media apps
- Todo list applications
- Chat applications
- Form submissions

## The `useOptimistic` Hook

React 19 introduces a new hook called `useOptimistic` that makes implementing optimistic UI patterns easier.

### Basic Syntax

```typescript
import { useOptimistic } from 'react';

// Basic usage
const [optimisticState, addOptimistic] = useOptimistic(
  originalState, 
  (currentState, optimisticValue) => {
    // Merge and return new state with optimistic value
    return newState;
  }
);
```

### Parameters

- `originalState`: The source of truth for your data
- `updateFunction`: A function that receives the current state and an optimistic value, and returns the updated state

### Return Values

- `optimisticState`: The current state with any optimistic updates applied
- `addOptimistic`: A function to trigger optimistic updates

## Basic Example: Counter

Here's a simple counter example with TypeScript:

```tsx
import { useState, useOptimistic } from 'react';

const Counter: React.FC = () => {
  // Original state
  const [count, setCount] = useState<number>(0);
  
  // Optimistic state
  const [optimisticCount, addOptimisticCount] = useOptimistic(
    count,
    (currentCount: number, incrementBy: number) => currentCount + incrementBy
  );

  // Simulated API call
  const updateCountOnServer = async (newCount: number): Promise<number> => {
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network delay
    return newCount;
  };

  const handleIncrement = async () => {
    // Update UI optimistically
    addOptimisticCount(1);
    
    try {
      // Actually update the server
      const updatedCount = await updateCountOnServer(count + 1);
      setCount(updatedCount);
    } catch (error) {
      // In case of error, the state will revert to the original count
      console.error('Failed to update count', error);
    }
  };

  return (
    <div>
      <p>Count: {optimisticCount}</p>
      <button onClick={handleIncrement}>Increment</button>
    </div>
  );
};
```

## Advanced Example: Todo List

A more realistic example with TypeScript for a todo list application:

```tsx
import { useState, useOptimistic, useRef } from 'react';

interface Todo {
  id: string;
  text: string;
  completed: boolean;
  isNew?: boolean; // Flag to indicate optimistic new items
  isDeleting?: boolean; // Flag to indicate optimistic deletions
}

const TodoApp: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([
    { id: '1', text: 'Learn React', completed: false }
  ]);
  
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (currentTodos, optimisticValue: { type: string; todo: Todo }) => {
      const { type, todo } = optimisticValue;
      
      switch (type) {
        case 'add':
          return [...currentTodos, { ...todo, isNew: true }];
        case 'delete':
          return currentTodos.map(item => 
            item.id === todo.id ? { ...item, isDeleting: true } : item
          );
        case 'toggle':
          return currentTodos.map(item => 
            item.id === todo.id ? { ...item, completed: !item.completed } : item
          );
        default:
          return currentTodos;
      }
    }
  );
  
  const inputRef = useRef<HTMLInputElement>(null);
  
  // Simulated API calls
  const addTodoToServer = async (todo: Todo): Promise<Todo> => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return { ...todo, id: Date.now().toString() };
  };
  
  const deleteTodoFromServer = async (id: string): Promise<string> => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return id;
  };
  
  const toggleTodoOnServer = async (todo: Todo): Promise<Todo> => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return { ...todo, completed: !todo.completed };
  };
  
  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputRef.current?.value.trim()) return;
    
    const newTodo: Todo = {
      id: 'temp-' + Date.now(),
      text: inputRef.current.value,
      completed: false
    };
    
    // Update UI optimistically
    addOptimisticTodo({ type: 'add', todo: newTodo });
    
    try {
      // Actually update the server
      const addedTodo = await addTodoToServer(newTodo);
      setTodos(prev => [...prev, addedTodo]);
      inputRef.current.value = '';
    } catch (error) {
      console.error('Failed to add todo', error);
      // No need to revert state as useOptimistic will do that automatically
    }
  };
  
  const handleDeleteTodo = async (todo: Todo) => {
    // Update UI optimistically
    addOptimisticTodo({ type: 'delete', todo });
    
    try {
      // Actually update the server
      await deleteTodoFromServer(todo.id);
      setTodos(prev => prev.filter(item => item.id !== todo.id));
    } catch (error) {
      console.error('Failed to delete todo', error);
    }
  };
  
  const handleToggleTodo = async (todo: Todo) => {
    // Update UI optimistically
    addOptimisticTodo({ type: 'toggle', todo });
    
    try {
      // Actually update the server
      const updatedTodo = await toggleTodoOnServer(todo);
      setTodos(prev => prev.map(item => 
        item.id === todo.id ? updatedTodo : item
      ));
    } catch (error) {
      console.error('Failed to toggle todo', error);
    }
  };
  
  return (
    <div>
      <h1>Todo List</h1>
      
      <form onSubmit={handleAddTodo}>
        <input 
          ref={inputRef} 
          type="text" 
          placeholder="Add new todo" 
        />
        <button type="submit">Add</button>
      </form>
      
      <ul>
        {optimisticTodos.map(todo => (
          <li 
            key={todo.id}
            style={{
              textDecoration: todo.completed ? 'line-through' : 'none',
              opacity: todo.isDeleting ? 0.5 : 1,
              backgroundColor: todo.isNew ? '#f0f8ff' : 'transparent'
            }}
          >
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => handleToggleTodo(todo)}
            />
            {todo.text}
            <button 
              onClick={() => handleDeleteTodo(todo)}
              disabled={todo.isDeleting}
            >
              Delete
            </button>
            {todo.isNew && <span> (Saving...)</span>}
            {todo.isDeleting && <span> (Deleting...)</span>}
          </li>
        ))}
      </ul>
    </div>
  );
};
```

## Using with Form Actions

React 19 also supports optimistic updates with form actions:

```tsx
import { useOptimistic, useRef } from 'react';

interface Message {
  text: string;
  sending?: boolean;
}

interface ThreadProps {
  messages: Message[];
  sendMessage: (message: string) => Promise<void>;
}

const ChatThread: React.FC<ThreadProps> = ({ messages, sendMessage }) => {
  const formRef = useRef<HTMLFormElement>(null);
  
  const [optimisticMessages, addOptimisticMessage] = useOptimistic(
    messages,
    (currentMessages: Message[], newMessage: string) => [
      ...currentMessages,
      {
        text: newMessage,
        sending: true
      }
    ]
  );
  
  const formAction = async (formData: FormData) => {
    const message = formData.get('message') as string;
    if (!message.trim()) return;
    
    // Update UI optimistically
    addOptimisticMessage(message);
    
    // Reset form
    formRef.current?.reset();
    
    // Send to server
    await sendMessage(message);
  };
  
  return (
    <div>
      <div className="messages">
        {optimisticMessages.map((message, index) => (
          <div key={index} className="message">
            {message.text}
            {message.sending && <span className="sending"> (Sending...)</span>}
          </div>
        ))}
      </div>
      
      <form ref={formRef} action={formAction}>
        <input 
          type="text" 
          name="message" 
          placeholder="Type a message..." 
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

// Parent component
const ChatApp: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hello there!" }
  ]);
  
  const sendMessage = async (text: string): Promise<void> => {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Update actual state after "server" processing
    setMessages(prev => [...prev, { text }]);
  };
  
  return <ChatThread messages={messages} sendMessage={sendMessage} />;
};
```

## Error Handling

One of the most important aspects of optimistic UI is proper error handling. When a server request fails, you need to revert the optimistic update:

```tsx
import { useState, useOptimistic } from 'react';

interface Post {
  id: string;
  title: string;
  likes: number;
  liking?: boolean;
}

const PostComponent: React.FC<{ post: Post }> = ({ post: initialPost }) => {
  const [post, setPost] = useState<Post>(initialPost);
  
  const [optimisticPost, addOptimisticPost] = useOptimistic(
    post,
    (currentPost, optimisticValue: { type: string; value?: any }) => {
      const { type, value } = optimisticValue;
      
      switch (type) {
        case 'like':
          return { ...currentPost, likes: currentPost.likes + 1, liking: true };
        default:
          return currentPost;
      }
    }
  );
  
  const likeFunctionThatMightFail = async (): Promise<Post> => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Simulate a random error
    if (Math.random() > 0.7) {
      throw new Error('Failed to like post');
    }
    
    return { ...post, likes: post.likes + 1 };
  };
  
  const handleLike = async () => {
    // Update UI optimistically
    addOptimisticPost({ type: 'like' });
    
    try {
      // Try to update on the server
      const updatedPost = await likeFunctionThatMightFail();
      setPost(updatedPost);
    } catch (error) {
      // On error, useOptimistic will revert to the original state
      console.error('Error liking post:', error);
      // Optionally show an error message
      alert('Failed to like the post. Please try again.');
    }
  };
  
  return (
    <div className="post">
      <h2>{optimisticPost.title}</h2>
      <button onClick={handleLike} disabled={optimisticPost.liking}>
        {optimisticPost.liking ? 'Liking...' : 'Like'} ({optimisticPost.likes})
      </button>
    </div>
  );
};
```

## Best Practices

1. **Keep optimistic updates simple**: Only update what's necessary for immediate feedback.

2. **Make error handling robust**: Always account for possible failures and provide feedback to users.

3. **Use visual indicators**: Slightly style optimistic items differently to indicate their temporary nature.

4. **Ensure consistent IDs**: Use temporary IDs for new items that can be replaced with server-generated IDs.

5. **Prevent duplicate actions**: Disable buttons or inputs during pending operations.

6. **Prioritize user experience**: The goal is to create a responsive app that feels instant.

## Considerations

- Optimistic UI works best for operations that rarely fail
- More complex for mutations that could have conflicts
- Test thoroughly to ensure good error recovery behavior
- Consider using along with React suspense or loading states for a comprehensive UI strategy

## Conclusion

The `useOptimistic` hook in React 19 provides a built-in way to implement optimistic UI patterns that were previously more cumbersome to achieve. By updating the UI immediately in response to user actions, you can create applications that feel faster and more responsive, enhancing the overall user experience.

Remember that optimistic updates are a UI pattern, not a replacement for proper data handling. Always ensure your application remains in a consistent state, especially when server operations fail.
