import { useNavigate } from "react-router-dom";
const SideBar = () => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/');
    }
    const contents = [
        {   
            id: 0,
            title: 'Connectors', 
            img: 'fa-brands fa-connectdevelop'
        }, 
        {
            id: 1,
            title: 'Sources', 
            img: 'fa-brands fa-osi'
        }, 
        {
            id: 2,
            title: 'Destinations',
            img: 'fa-solid fa-location-dot'
        }, 
        {
            id: 3,
            title: 'Builder',
            img:'fa-solid fa-screwdriver-wrench'
        }
    ]

    return (
        <nav className='w-[100px] px-[3px] py-[20px] relative h-full bg-white flex flex-col items-center'>
            <div>
                <div className='flex items-center justify-center' onClick={handleClick}>
                    <img
                        src='https://media.licdn.com/dms/image/D560BAQHO3q9m2okBUQ/company-logo_200_200/0/1686938244217?e=1695254400&v=beta&t=WQb9XCduLnzmlUPgEYvjI0WnsLkqoMVTWATMuFUwFgE'
                        alt='logo'
                        className='w-1/2 h-1/2'
                    />
                </div>
            </div>
            {/* <ul>
                {
                    contents.map(content => 
                        <li
                            key={content.id}
                            className='w-full flex flex-col justify-center items-center h-[70px] rounded-lg hover:bg-gray-100 my-2 cursor-pointer text-purple-900 text-md'
                        >
                            <i
                                className={content.img}
                            />
                            <span>
                                {content.title}
                            </span>
                        </li>
                    )
                }
            </ul> */}
        </nav>
    )
};

export default SideBar;
