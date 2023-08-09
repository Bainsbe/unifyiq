import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import * as connectorAction from '../../../store/connectorReducer';
import {
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Td,
    TableContainer,
    Switch, 
    Button
} from '@chakra-ui/react'
import { useNavigate } from 'react-router-dom';

const ContentTable = () => {
    const headers = ['name', 'connector type', 'url prefix', 'start time', 'last fetched', 'is enabled?', ''];
    const { connectors, loading } = useSelector(state => state.connectors)
    const [update, setUpdate] = useState({});
    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(connectorAction.listConnectors()); 
    },[dispatch])
    const navigate = useNavigate();
    const handleUpdate = (i,id) => () => {
        const newUpdate = {
            ...update,
            [i]: !update[i]
        };
        setUpdate(newUpdate);
        navigate(`/connections/${id}`);
    }
    return (
        <div className='p-5'>
            <TableContainer className='bg-white rounded-lg'>
                <Table size='sm'>
                    <Thead>
                        <Tr>
                            {
                                headers.map(header => 
                                    <Th key={header}>
                                        {header}
                                    </Th>
                                )
                            }
                        </Tr>
                    </Thead>
                    <Tbody className='hover:bg-gray-50 cursor-pointer'>
                        {   connectors.length > 0 &&
                            connectors.map((connector,i) =>
                                <Tr key={connector.id}>
                                    <Td>{connector.name}</Td>
                                    <Td>{connector.connector_type}</Td>
                                    <Td>{connector.url_prefix}</Td>
                                    <Td>{connector.start_ts}</Td>
                                    <Td>{connector.last_fetched_ts}</Td>
                                    <Td>{connector.is_enabled}</Td>
                                    <Td>
                                        <Button i={i}
                                            onClick={handleUpdate(i, connector.id)}
                                            colorScheme='purple'
                                            size='sm'
                                        >
                                            Update
                                        </Button>
                                    </Td>
                                </Tr>)
                        }
                    </Tbody>
                </Table>
            </TableContainer>
        </div>
    )
};

export default ContentTable;
