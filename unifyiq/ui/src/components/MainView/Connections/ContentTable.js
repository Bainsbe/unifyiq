import { useEffect } from 'react'
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
    Switch
  } from '@chakra-ui/react'

const ContentTable = () => {
    const headers = ['name', 'connector type', 'url prefix', 'start time', 'last fetched', 'is enabled?'];
    const { connectors, loading } = useSelector(state => state.connectors)
    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(connectorAction.listConnectors()); 
    },[dispatch])

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
                            connectors.map(connector =>
                                <Tr key={connector.id}>
                                    <Td>{connector.name}</Td>
                                    <Td>{connector.connector_type}</Td>
                                    <Td>{connector.url_prefix}</Td>
                                    <Td>{connector.start_ts}</Td>
                                    <Td>{connector.last_fetched_ts}</Td>
                                    <Td>{connector.is_enabled}</Td>
                                </Tr>)
                        }
                    </Tbody>
                </Table>
            </TableContainer>
        </div>
    )
};

export default ContentTable;
