import { ChakraProvider } from '@chakra-ui/react'
import {Routes, Route} from 'react-router-dom'
import SideBar from './components/SideBar'
import MainView from './components/MainView'
import NewConnection from './components/MainView/Connections/NewConnection'
import { Login } from './components/Login'
import { Navigate, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import jwt_decode from 'jwt-decode'
function App() {
  function RequireAuth({ children, redirectTo }) {
    const navigate = useNavigate()
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    useEffect(() => {
      const token = localStorage.getItem('token');
      if (token) {
        const decodedToken = jwt_decode(token);
        const tokenExpiredTime = decodedToken.exp * 1000;
        const currentTime = Date.now();
        if (currentTime < tokenExpiredTime) {
          setIsAuthenticated(true);
          navigate('/')
        } else {
          setIsAuthenticated(false);
          localStorage.removeItem('token');
          navigate('/login');
        }
      } else {
        setIsAuthenticated(false);
        navigate('/login');
      }
    }, [navigate]);

    return isAuthenticated ? children : <Navigate to={redirectTo} />;
  }

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

export default App;
