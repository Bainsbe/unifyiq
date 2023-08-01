import {
    Card,
    CardBody,
    Heading,
    Select,
    Stack,
    FormControl,
    FormLabel,
    Input,
    CardFooter,
    Button,
    Text
} from '@chakra-ui/react'
import * as connectorAction from '../../../../store/connectorReducer'
import {SLACK, CONFLUENCE, GOOGLEDOC} from "../../../../constants";

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {useDispatch} from 'react-redux'


function isValidUrl(url) {
    const urlRegex = /^(?:(?:https?|ftp):\/\/)?(?:www\.)?[a-z0-9\-]+\.[a-z]{2,}(?:\.[a-z]{2,})?(?:\/.*)?$/i;
    return urlRegex.test(url);
  }

const NewForm = () => {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [source, setSource] = useState(SLACK);
    const [url, setUrl] = useState('');
    const [date, setDate] = useState('');
    const [nameErr, setNameErr] = useState('');
    const [urlErr, setUrlErr] = useState('');
    const [dateErr, setDateErr] = useState('');
    const [err, setErr] = useState('');
    const dispatch = useDispatch();
    const [config, setConfig] = useState();
    const [configSettings, setConfigSettings] = useState({});
    const [configValues, setConfigValues] = useState([]);
    const [configErrors, setConfigErrors] = useState({});

    useEffect(() => {
        //potential bug is if the name of the source != the name in options
        //ensure constants in constants.js are the same as constants.py
        setConfig(configSettings[source]);
    }, [source, setConfig, configSettings]);

    useEffect(() => {
        fetch('/api/v1/connectors/fetcher_config_values', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }
        )
            .then(response => response.json())
            .then(data => {
                setConfigSettings(data)
                setConfig(data[source])
            })
            .catch(error => console.error('Error:', error));
    }, [source])

    const handleConfigChange = (name) => (e) => {
        const {value} = e.target;
        setConfigValues({
            ...configValues,
            [name]: value
        })
    }
    const handleSelectChange = (e) => {
        setSource(e.target.value);
        setConfig(configSettings[e.target.value]);
    }

    const handleSubmit = async () => {
        setNameErr('');
        setUrlErr('');
        setDateErr('');
        setErr('');
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

        // This will check all the config fields to ensure none of them are empty.
        Object.entries(configValues).forEach(([key, value]) => {
            if (!value || value.trim() === '') {
                errorObject[key] = true;
            }
        });

        setConfigErrors(errorObject);

        // Check if we have any error, if so, return and don't submit the form.
        if (Object.keys(errorObject).length > 0) return;


        if (name.trim() !== '' && name.length <= 45 && url.trim() !== '' && isValidUrl(url) && date.trim() !== '') {
            const info = {
                name,
                connector_type: source,
                url_prefix: url,
                start_ts: new Date(date).getTime() / 1000,
                is_enabled: true,
                last_fetched_ts: 0,
                config_json: configValues
            }
            const data = await dispatch(connectorAction.addConnectors(info));
            if (data.payload.status === 'success') {
                return navigate('/');
            } else {
                setErr('Something went wrong. Please try again.')
            }
        }
    }

    return (
        <div className='my-[15px] mx-auto px-3 w-full h-full flex flex-col items-center'>
            <div className='w-full p-8'>
                <Card
                    size='md'
                    colorScheme='purple'
                >
                    <CardBody>
                        <Stack spacing='24px'>
                            <Heading size='md'>
                                Set up a new source
                            </Heading>
                            <FormControl>
                                <FormLabel>Name</FormLabel>
                                <Input
                                    placeholder='UnifyIQ'
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    isRequired={true}
                                    isInvalid={nameErr !== ''}
                                />
                                {
                                    nameErr !== '' && <Text color='red' className='mt-2'>{nameErr}</Text>
                                }
                            </FormControl>
                            <FormControl>
                                <FormLabel>
                                     Source type
                                 </FormLabel>
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
                            </FormControl>
                            {
                                (config && config.configs.map((item, index) => (
                                    <FormControl key={index}>
                                        <FormLabel>{item.display_name}</FormLabel>
                                        <Input
                                            placeholder={`Enter ${item.display_name}`}
                                            value={configValues[item.name]}
                                            isRequired={true}
                                            isInvalid={configErrors[item.name]}
                                            onChange={handleConfigChange(item.name)}
                                        />
                                        {
                                            configErrors[item.name] && <Text color='red' className='mt-2'>This field is required</Text>
                                        }
                                    </FormControl>
                                )))
                            }
                            <FormControl>
                                <FormLabel>URL prefix</FormLabel>
                                <Input
                                    type='url'
                                    placeholder='https://example.com'
                                    value={url}
                                    onChange={(e) => setUrl(e.target.value)}
                                    isInvalid={urlErr !==''}
                                />
                                {
                                    urlErr !== '' && <Text color='red' className='mt-2'>{urlErr}</Text>
                                }
                            </FormControl>
                            <FormControl>
                                <FormLabel>Source Start Time</FormLabel>
                                <Input
                                    type='date'
                                    value={date}
                                    onChange={(e) => setDate(e.target.value)}
                                    isInvalid={dateErr !== ''}
                                />
                                {
                                    dateErr !== '' && <Text color='red' className='mt-2'>{dateErr}</Text>
                                }
                            </FormControl>
                        </Stack>
                    </CardBody>
                    <CardFooter>
                        <Button colorScheme='purple' onClick={handleSubmit}>Set up source</Button>
                    </CardFooter>
                </Card>
            </div>
        </div>
    )
};

export default NewForm;
