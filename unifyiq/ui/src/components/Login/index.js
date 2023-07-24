import {
    Text,
    Heading,
    Card,
    CardBody, 
    FormControl,
    Stack,
    Input,
    InputGroup,
    InputRightElement,
    Button,
    CardFooter
} from '@chakra-ui/react'

import { useState } from 'react'

function isValidEmail(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    return pattern.test(email);
}
export const Login = () => {
    const [show, setShow] = useState(false);
    const [activated, setActivated] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [emailErr, setEmailErr] = useState('');
    const [passwordErr, setPasswordErr] = useState('');

    const handleClickShow = () => {
        setShow(!show);
    }

    const handleClickActivate = () => {
        setActivated(!activated);
    }

    const handleClickLogin = () => {
        let emailErr = '';
        let passwordErr = '';
        setEmailErr('');
        setPasswordErr('');
        if (email.trim() === '' || !isValidEmail(email)) {
            emailErr = 'Please enter a valid email.';
        }
        if (password.trim() === '') {
            passwordErr = 'Please enter a password.';
        } else if (password.length < 8 || password.length > 20) {
            passwordErr = 'Password must be between 8 and 20 characters.';
        }
        if (emailErr || passwordErr) {
            setEmailErr(emailErr);
            setPasswordErr(passwordErr);
            return; 
        }
        console.log('login successful');
        return;
    }
    return (
        <div className='w-full h-full bg-gray-50 flex flex-col'>
            <div className='flex flex-row justify-center h-[200px] items-center'>
                <img
                    src='https://media.licdn.com/dms/image/D560BAQHO3q9m2okBUQ/company-logo_200_200/0/1686938244217?e=1695254400&v=beta&t=WQb9XCduLnzmlUPgEYvjI0WnsLkqoMVTWATMuFUwFgE'
                    alt='logo'
                    className='w-12 h-12'
                />
                <Heading>
                    UnifyIQ
                </Heading>
            </div>
            <div className='flex w-full h-full justify-center'>
                <div className='w-1/2'>
                    {
                        !activated &&
                        <Card size='md'>
                            <CardBody>
                                <Stack spacing='24px'>
                                    <Heading
                                        size='md'
                                        className='text-center'
                                    >Login to UnifyIQ</Heading>
                                    <FormControl>
                                        <Input
                                            type='email'
                                            placeholder='Email'
                                            isInvalid={emailErr !== ''}
                                        />
                                        {
                                            emailErr !== '' && <Text color='red'>{emailErr}</Text>

                                        }                                    
                                    </FormControl>
                                    <FormControl>
                                        <InputGroup>
                                            <Input
                                                type={show ? 'text' : 'password'}
                                                placeholder='Enter password'
                                                required
                                                isInvalid={passwordErr !== ''} 
                                            />
                                            <InputRightElement>
                                                <Button w='10rem' m='2px' size='sm' onClick={handleClickShow}>
                                                    {show ? 'Hide': 'Show'}
                                                </Button>
                                            </InputRightElement>
                                        </InputGroup>
                                        {
                                            passwordErr !== '' && <Text color='red'>{passwordErr}</Text>

                                        }   
                                    </FormControl>
                                </Stack>
                            </CardBody>
                            <CardFooter className='flex justify-center flex-col' >
                                <Button colorScheme='purple' onClick={handleClickLogin}>Login</Button>
                                <Text  className='text-center mt-2 cursor-pointer' onClick={handleClickActivate}>Activate Email</Text>
                            </CardFooter>
                        </Card>
                    }
                    {
                        activated && 
                        <Card size='md'>
                            <CardBody>
                                <Stack spacing='24px'>
                                    <Heading
                                        size='md'
                                        className='text-center'
                                    >Login to UnifyIQ</Heading>
                                    <FormControl>
                                        <Input
                                            type='email'
                                            placeholder='Email'
                                            isInvalid={emailErr !== ''}
                                        />
                                        {
                                            emailErr !== '' && <Text color='red'>{emailErr}</Text>

                                        }                                    
                                    </FormControl>
                                </Stack>
                            </CardBody>
                            <CardFooter className='flex justify-center flex-col' >
                                <Button colorScheme='purple'>Activate account</Button>
                                <Text  className='text-center mt-2 cursor-pointer' onClick={handleClickActivate}>Activated already? Login</Text>
                            </CardFooter>
                        </Card>
                    }
                   
                </div>
            </div>
            
        </div>
    )
}
