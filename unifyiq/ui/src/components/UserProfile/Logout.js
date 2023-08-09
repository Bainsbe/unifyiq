import {
    Button
} from '@chakra-ui/react'
import * as sessionAction from '../../store/sessionReducer'
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';


const Logout = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const handleLogout = async() => {
        const res = await dispatch(sessionAction.logout());
        if (res.payload) {
            const data = res.payload; 
            if (data.msg) {
                navigate('/login');
            } else {
                console.log('error')
            }
        }
    }
    return (
        <div className='absolute left-24 border flex justify-center top-0 w=[100px]' >
            <Button colorScheme='purple' onClick={handleLogout}>Log out</Button>
        </div>
    )
}

export default Logout;
