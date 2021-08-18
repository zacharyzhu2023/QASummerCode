import * as FaIcons from 'react-icons/fa';
import * as IoIcons from 'react-icons/io';

// All the buttons on the sidebar
export const SidebarData = [
    {
        title: 'Dashboard',
        path: '/',
        icon: <FaIcons.FaTachometerAlt />,
        className: 'bar-item'
    }, 
    {
        title: 'Form',
        path: '/form',
        icon: <FaIcons.FaFileAlt />,
        className: 'bar-item'
    }, 
    {
        title: 'Settings',
        path: '/settings',
        icon: <FaIcons.FaCogs />,
        className: 'bar-item'
    }, 
]