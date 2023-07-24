import { Route, useNavigate } from "react-router-dom"

const ProtectedRoute = (props) => {
    const navigate = useNavigate('/login');
    const user = 'user'
    return (
        <Route {...props}>
            {user ? props.children : navigate('/login')}
        </Route>
    )
}

export default ProtectedRoute;
