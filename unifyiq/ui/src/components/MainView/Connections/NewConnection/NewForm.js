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

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {useDispatch} from 'react-redux'


function isValidUrl(url) {
    const urlRegex = /^(?:(?:https?|ftp):\/\/)?(?:www\.)?[a-z0-9\-]+\.[a-z]{2,}(?:\/.*)?$/i;
        return urlRegex.test(url);
  }

const NewForm = () => {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [source, setSource] = useState('Slack'); 
    const [url, setUrl] = useState('');
    const [date, setDate] = useState('');
    const [nameErr, setNameErr] = useState('');
    const [urlErr, setUrlErr] = useState('');
    const [dateErr, setDateErr] = useState('');
    const [err, setErr] = useState('');
    const dispatch = useDispatch();

    const options = [ 
        {
            id: 0, 
            source: 'Slack', 
            logo: 'test'
        }, 
        {
            id: 1, 
            source: 'GoogleDoc', 
            logo: 'test'
        }, 
        {
            id: 2,
            source: 'ConfluenceWiki',
            logo: 'test'
        }
    ]

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
        if (name.trim() !== '' && name.length <= 45 && url.trim() !== '' && isValidUrl(url) && date.trim() !== '') {
            const info = {
                name,
                connector_type: source,
                url_prefix: url,
                start_ts: new Date(date).getTime() / 1000,
                is_enabled: true,
                last_fetched_ts: 0
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
                                    onChange={(e)=> setSource(e.target.value)}
                                >
                                    {
                                        options.map(option =>
                                            <option key={option.id}>{option.source}</option>
                                        )
                                    }
                                </Select>
                            </FormControl>
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
