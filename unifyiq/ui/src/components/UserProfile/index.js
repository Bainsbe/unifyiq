import { useState } from 'react'
import Logout from './Logout';

const UserProfile = () => {
    const [show, setShow] = useState(false);

    const handleClick = () => {
        setShow(!show)
    }

    return (
        <div className='relative'>
            <div onClick={handleClick}>
                <i className='fa-solid fa-user cursor-pointer'></i>
            </div>
            {
                show && <Logout/>
            }
        </div>
       
    )
}

export default UserProfile
