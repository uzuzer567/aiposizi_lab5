import React from 'react';
import {
    Link
} from 'react-router-dom'


const SECTIONS = [
    {title: 'Documents', href: '/documentsTable'},
    {title: 'Factories', href: '/factoriesTable'},
    {title: 'Tasks', href: '/tasksTable'},
    {title: 'Users', href: '/usersTable'},

    {title: 'Add document', href: '/addDocument'},
    {title: 'Add user', href: '/addUser'},
    {title: 'Add factory', href: '/addFactory'},
    {title: 'Add task', href: '/addTask'},
]


class Home extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            'sections': SECTIONS,
            'is_logged': true
        }
    }

    logoutUser = () => {
        sessionStorage.removeItem('token');

        this.props.history.push('/login')
    }

    render() {
        const { sections } = this.state

        let all_links = []

        for (let i=0; i < sections.length; i++){
            let curr_section = SECTIONS[i]

            all_links.push(
                <Link className='button-link' to={curr_section['href']}>
                    {curr_section['title']}
                </Link>
            )
        }

        let links_element = (
            <div>
                {all_links}

                <button className='button-link'
                        onClick={ this.logoutUser.bind(this) }
                        style={{float: 'right'}}>
                    Logout
                </button>
            </div>
        );

        return links_element
    }
}


export default Home;
