import { ChakraProvider } from '@chakra-ui/react'
import {Routes, Route} from 'react-router-dom'
import SideBar from './components/SideBar'
import MainView from './components/MainView'
import NewConnection from './components/MainView/Connections/NewConnection'
import { Login } from './components/Login'
import { Navigate } from 'react-router-dom'

function App() {
  return (
    <ChakraProvider>
      <Routes>

          <Route
            path='/'
            element={
              <RequireAuth redirectTo='/login'>
                <div className='App flex flex-row w-full h-full'>
                  <SideBar />
                  <MainView/>
               </div>
              </RequireAuth>       
            }
            >
            </Route>
        <Route
          path='/login'
          element={
            <div className='App flex flex-row w-full h-full'>
              <SideBar />
              <Login/>
            </div>
          }
        >
        </Route>
        <Route
          path='/connections/new'
          element={
            <div className='App flex flex-row w-full h-full'>
              <SideBar />
              <NewConnection/>
            </div>
          }
        />
        
        
      </Routes>
    </ChakraProvider>
  );
}
function RequireAuth({ children, redirectTo }) {
  let isAuthenticated = localStorage.getItem('token');
  return isAuthenticated ? children : <Navigate to={redirectTo} />;
}

export default App;
