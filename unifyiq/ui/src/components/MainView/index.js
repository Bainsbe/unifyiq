import PageHeader from '../PageHeader'
import ContentTable from './Connections/ContentTable'
const MainView = () => {
    return (
        <div className='w-full h-full bg-gray-100 flex flex-col'>
            <PageHeader title='connectors' link='connections/new' hidden={false} />
            <ContentTable/>
        </div>
    )
};

export default MainView;
