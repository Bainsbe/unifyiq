import {Button} from '@chakra-ui/react'
import { BsPlusLg } from 'react-icons/bs'
import { useNavigate } from 'react-router-dom'

const PageHeader = ({ title, link, hidden }) => {
    const navigate = useNavigate();

    const routeChange = (link) => {
        navigate(`/${link}`);
    }

    const handleClick = () => {
        routeChange(link);
    }
    return (
        <div>
            <div className='flex flex-row justify-between pb-0 pt-5 px-5'>
                <h1 className='text-[20px] text-black font-bold uppercase'>{title}</h1>
                {
                    !hidden && 
                    <Button
                        leftIcon={<BsPlusLg/>}
                        colorScheme='purple'
                        variant='solid'
                        size='sm'
                        onClick={handleClick}
                    >
                        New {title}
                    </Button>
                }
            </div>
        </div>
    )
}

export default PageHeader;
