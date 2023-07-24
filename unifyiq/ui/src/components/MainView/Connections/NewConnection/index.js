import PageHeader from "../../../PageHeader"
import FormPage from "./FormPage"
const NewConnection = () => {
    return (
        <div className='w-full h-full bg-gray-50'>
            <PageHeader title='New Connector' hidden={true} />
            <FormPage/>
        </div>
    )
}

export default NewConnection;
