import { ChakraProvider } from '@chakra-ui/react'
import {Routes, Route} from 'react-router-dom'
import SideBar from './components/SideBar'
import MainView from './components/MainView'
import NewConnection from './components/MainView/Connections/NewConnection'
import { Login } from './components/Login'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

function App() {
  // const [loaded, setLoaded] = useState(false); 

  // useEffect(() => {
    
  // })
  // if (!loaded) {
  //   return null;
  // }



  return (
    <ChakraProvider>
      <Routes>
        <Route
          path='/'
          element={
            <div className='App flex flex-row w-full h-full'>
              <SideBar />
              <MainView/>
            </div>
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
