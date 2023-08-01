import {
    Text,
    Heading,
    Card,
    CardBody, 
    FormControl,
    Stack,
    Input,
    HStack, 
    PinInput,
    PinInputField,
    Button,
    CardFooter
} from '@chakra-ui/react'
import { useState } from 'react'
import * as sessionAction from '../../store/sessionReducer'
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';


function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
export const Login = () => {
    const [next, setNext] = useState(false);
    const [email, setEmail] = useState('');
    const [emailErr, setEmailErr] = useState('');
    const [digit1, setDigit1] = useState('');
    const [digit2, setDigit2] = useState('');
    const [digit3, setDigit3] = useState('');
    const [digit4, setDigit4] = useState(''); 
    const [digit5, setDigit5] = useState('');
    const [digit6, setDigit6] = useState('');
    const [verifiedErr, setVerifiedErr] = useState('');
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleClickContinue = async() => {
        let emailErr = '';
        let passwordErr = '';
        setEmailErr('');
        setVerifiedErr('');
        if (email.trim() === '' || !email) {
          emailErr = 'Please enter a valid email.';
        } 
        if (!isValidEmail(email)) {
            emailErr = 'Please enter a valid email.';
        }
        if (emailErr || passwordErr) {
          setEmailErr(emailErr);
          return; 
        }
        const response = await dispatch(sessionAction.verifiedEmail(email)); 
        if (response.payload) {
            const data = response.payload; 
            if (data.error) {
                setVerifiedErr(data.error)
            } else {
                setNext(true);
            }
        }
        
    };
    
    const handleCLickSubmit = async () => {
        setVerifiedErr('');
        const time = Date.now() / 1000;
        const otp = digit1 + digit2 + digit3 + digit4 + digit5 + digit6; 
        const response = await dispatch(sessionAction.login({ time, otp, email })); 
        if (response.payload) {
            const data = response.payload; 
            if (data.message) {
                navigate('/');
            } else {
                setVerifiedErr(data.error);
            }
        }
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
                        !next &&
                        <Card size='md'>
                            <CardBody>
                                    <Stack spacing='24px'>
                                        <Heading
                                        size='md'
                                        className='text-center'
                                        >Login to UnifyIQ</Heading>
                                        <Text color='red' as='b' className='flex justify-center'> {verifiedErr}</Text>
                            
                                        <FormControl>
                                            <Input
                                                type='email'
                                                placeholder='Email'
                                                isInvalid={emailErr !== ''}
                                                value={email}
                                                onChange={e => setEmail(e.target.value)}    

                                            />
                                            {
                                                emailErr !== '' && <Text color='red'>{emailErr}</Text>

                                            }                                    
                                        </FormControl>
                                    </Stack>
                                </CardBody>
                                <CardFooter className='flex justify-center flex-col' >
                                    <Button colorScheme='purple' onClick={handleClickContinue}>Continue</Button>
                                </CardFooter>
                        </Card>
                    }
                    {
                        next && 
                        <Card size='md'>
                            <CardBody>
                                <Stack spacing='24px'>
                                    <Heading
                                        size='md'
                                        className='text-center'
                                    >
                                        Please confirm your OTP
                                    </Heading>
                                    <Text>
                                        Enter the OTP we sent to your email. Please check junk mail  if it's not in your inbox        
                                    </Text>    
                                    <HStack className='flex justify-center'>
                                        <PinInput>
                                                <PinInputField
                                                    value={digit1}
                                                    onChange={e => setDigit1(e.target.value)}
                                                />
                                                <PinInputField
                                                    value={digit2}
                                                    onChange={e => setDigit2(e.target.value)}
                                                />
                                                <PinInputField
                                                    value={digit3}
                                                    onChange={e => setDigit3(e.target.value)}
                                                />
                                                <PinInputField
                                                    value={digit4}
                                                    onChange={e => setDigit4(e.target.value)}
                                                />
                                                <PinInputField
                                                    value={digit5}
                                                    onChange={e => setDigit5(e.target.value)}
                                                />
                                                <PinInputField
                                                    value={digit6}
                                                    onChange={e => setDigit6(e.target.value)}
                                                />
                                        </PinInput>
                                    </HStack>
                                    </Stack>
                                    
                                </CardBody>
                                <Text color='red' className='flex justify-center'>{verifiedErr}</Text>    
                            <CardFooter className='flex justify-center flex-col' >
                                    <Button colorScheme='purple' onClick={handleCLickSubmit}>Submit</Button>
                                    {verifiedErr && 
                                    <Text className='flex justify-center my-[12px] cursor-pointer'>Resend OTP</Text>
                                    }
                            </CardFooter>
                        </Card>
                    }
                   
                </div>
            </div>
            
        </div>
    )
}
