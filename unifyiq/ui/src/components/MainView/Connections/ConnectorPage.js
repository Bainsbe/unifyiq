import {
    Input,
    Button,
    Text,
    TableContainer,
    Tr,
    Td,
    Tbody,
    Table,
    Switch,
    ButtonGroup,
    Select,
    FormControl
} from '@chakra-ui/react'
import PageHeader from '../../PageHeader'
import { useNavigate, useParams,  } from 'react-router-dom'
import { useState, useEffect } from 'react'
import * as connectorAction from '../../../store/connectorReducer'
import {useDispatch, useSelector} from 'react-redux'
import {SLACK, CONFLUENCE, GOOGLEDOC} from '../../../constants'

function isValidUrl(url) {
    const urlRegex = /^(?:(?:https?|ftp):\/\/)?(?:www\.)?[a-z0-9\-]+\.[a-z]{2,}(?:\.[a-z]{2,})?(?:\/.*)?$/i;
    return urlRegex.test(url);
}
const ConnectorPage = () => {
    const navigate = useNavigate();
    const [err, setErr ] = useState('');
    const [success, setSuccess ] = useState('');
    const [name, setName] = useState('');
    const [source, setSource] = useState('');
    const [url, setUrl] = useState('');
    const [date, setDate] = useState('');
    const [nameErr, setNameErr] = useState('');
    const [urlErr, setUrlErr] = useState('');
    const [dateErr, setDateErr] = useState('');
    const [config, setConfig] = useState();
    const [configSettings, setConfigSettings] = useState({});
    const [configValues, setConfigValues] = useState({});
    const [configErrors, setConfigErrors] = useState({});
    const dispatch = useDispatch();
    const [connector, setConnector] = useState({})
    const handleCancel = () => {
        navigate('/');
        return;
    }
    const { id } = useParams();
    const handleSelectChange = (e) => {
        setSource(e.target.value);
        setConfig(configSettings[e.target.value]);
    }
    const handleConfigChange = (name) => (e) => {
        const {value} = e.target;
        setConfigValues({
            ...configValues,
            [name]: value
        })
    }
    const handleUpdate = async() => {
        setNameErr('');
        setUrlErr('');
        setDateErr('');
        setErr('');
        setConfigErrors('');
        if (name.trim() === '' || name.length > 45) {
            setNameErr('Name can not be empty or longer than 45 characters.');
        }
        if (url.trim() === '' || !isValidUrl(url)) {
            setUrlErr('URL can not be empty or invalid.');
        }
        if (date.trim() === '') {
            setDateErr('Date cannot be empty.');
        }

        let errorObject = {};
        
        Object.entries(configValues).forEach(([key, value]) => {           
            if ((!value || value.trim() === '')) {
                errorObject[key] = true;
            } 
        });
        
        
        setConfigErrors(errorObject);

        // Check if we have any error, if so, return and don't submit the form.
        if (Object.keys(errorObject).length > 0) {
            return
        } 


        if (name.trim() !== '' && name.length <= 45 && url.trim() !== '' && isValidUrl(url) && date.trim() !== '') {
            const info = {
                id,
                name,
                connector_type: source,
                url_prefix: url,
                start_ts: new Date(date).getTime() / 1000,
                is_enabled: true,
                last_fetched_ts: 0,
                config_json: configValues
            }
           
            const data = await dispatch(connectorAction.updateConnector(info));
            console.log(data)
            if (data.payload && data.payload.msg === 'Successfully update') {
                return navigate('/');
            } else {
                setErr('Something went wrong. Please try again.')
            }
        }
    }
    useEffect(() => {
        const response = dispatch(connectorAction.getConnector(id))
            .then(response => {
                // response.json()
                const connector = response.payload;
                let data = {}
                if (connector.config_json !== null) {
                    data = JSON.parse(connector.config_json);
                } 
               
                const dateData = connector.start_ts; 
                const date = new Date(dateData * 1000);
                const formattedDate = date.toISOString().split('T')[0];
                setConnector(connector);
                setName(connector.name); 
                setUrl(connector.url_prefix);
                setDate(formattedDate);
                setSource(connector.connector_type);
                setConfigValues(data);
            });
    },[dispatch, id, setConfig, setConnector, setName, setUrl, setDate, setSource])

    useEffect(() => {
        fetch('/api/v1/connectors/fetcher_config_values', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
        )
            .then(response => response.json())
            .then(data => {
                console.log(data)
                setConfigSettings(data)
                setConfig(data[source])
            })
            .catch(error => console.error('Error:', error));
    }, [source])

    return (
        <div className='w-full h-full bg-gray-50 flex flex-col px-6'>
            <PageHeader title='Connector' link='connections/detail' hidden={true} />
            <div className='h-[20px]'></div>
            <div className='flex w-full'>
                <TableContainer className='w-full px-2'>
                    <Table size='lg'>
                        <Tbody>
                            {
                                connector && 
                                    <>
                                        <Tr>
                                            <Td className='font-bold w-1/4'>
                                                Name
                                            </Td>
                                            <Td>
                                                <FormControl>
                                                    <Input
                                                        placeholder={connector.name}
                                                        variant='unstyled'
                                                        type='text'
                                                        value={name}
                                                        onChange={e => setName(e.target.value)}
                                                        isInvalid={nameErr !== ''}
                                                />
                                                </FormControl>

                                            </Td>
                                            <Td>
                                            {
                                                nameErr !== '' && <Text color='red' className='mt-2'>{nameErr}</Text>
                                            }
                                            </Td>
                                        </Tr>
                                        <Tr>
                                            <Td className='font-bold w-1/4'>
                                                Connector Type
                                            </Td>
                                            <Td>
                                                <Select
                                                     value={source}
                                                     onChange={handleSelectChange}
                                                     isRequired={true}
                                            >
                                                {
                                                    (configSettings && Object.entries(configSettings).map(([name_key, configs], index) =>
                                                        <option key={index} value={name_key}>
                                                            {configs.display_name}
                                                        </option>
                                                    ))
                                                }
                                             
                                            </Select>
                                            </Td> 
                                       
                                        </Tr>
                                        {
                                            (Object.keys(configValues).length >= 0 && config && config.configs.map((item, index) => (
                                               <Tr>
                                                    <Td className='font-bold w-1/4'>{item.display_name}</Td>
                                                    <Td>
                                                        <FormControl>
                                                            <Input
                                                                placeholder={configValues[item.name] ? `${configValues[item.name]}` : `Enter ${item.display_name}`}
                                                                value={configValues[item.name]}
                                                                isRequired={true}
                                                                isInvalid={configErrors[item.name]}
                                                                onChange={handleConfigChange(item.name)}
                                                                variant='unstyled'
                                                            />
                                                        </FormControl>
                                                    </Td>
                                                    {
                                                        configErrors[item.name] && <Text color='red' className='mt-2'>This field is required</Text>
                                                    }
                                               </Tr>
                                            )))
                                        }
                                        <Tr>
                                            <Td className='font-bold w-1/4'>
                                                Start Time
                                            </Td>
                                            <Td>
                                                <FormControl>
                                                    <Input
                                                        variant='unstyled'
                                                        type='date'
                                                        value={date}
                                                        onChange={e => setDate(e.target.value)}
                                                />
                                                </FormControl>
                                            </Td>
                                            <Td>
                                                {
                                                    dateErr !== '' && <Text color='red' className='mt-2'>{dateErr}</Text>
                                                }
                                            </Td>
                                        </Tr>
                                        <Tr>
                                            <Td className='font-bold w-1/4'>
                                                URL PREFIX	
                                            </Td>
                                            <Td>
                                                <FormControl>
                                                    <Input
                                                        placeholder={connector.url_prefix}
                                                        variant='unstyled'
                                                        type='text'
                                                        value={url}
                                                        onChange={e => setUrl(e.target.value)}
                                                />
                                                </FormControl>
                                            </Td>
                                            <Td>
                                                {
                                                    urlErr !== '' && <Text color='red' className='mt-2'>{urlErr}</Text>
                                                }
                                            </Td>
                                        </Tr>
                                        <Tr>
                                            <Td className='font-bold w-1/4'>
                                                Is Enabled?
                                            </Td>
                                            <Td>
                                                <Switch size='lg' isChecked={connector.is_enabled} 
                                                
                                                ></Switch>
                                            </Td>
                                        </Tr>
                                    </>
                            }
                            
                        </Tbody>
                    </Table>
                </TableContainer>
            </div>
            <div className='h-[30px]'>
                {
                    err && <Text>{err}</Text>
                }
                {
                    success && <Text>{success}</Text>
                }
            </div>
            <div className='w-full flex justify-end p-4'>
                <ButtonGroup>
                    <Button colorScheme='purple' onClick={handleUpdate}> 
                        Update
                    </Button>
                    <Button onClick={handleCancel}>
                        Cancel
                    </Button>
                </ButtonGroup>
            </div>
        </div>
    )
}

export default ConnectorPage
