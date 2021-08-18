import * as FaIcons from 'react-icons/fa';
import * as AiIcons from 'react-icons/ai';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import { SidebarData } from './SidebarData';
import './Sidebar.css';
import { IconContext  } from 'react-icons';

// Sidebar for navigating to different pages
function Sidebar() {
    const [sidebar, setSidebar] =  useState(false);
    const showSidebar = () => setSidebar(!sidebar);

    return (
        <IconContext.Provider value={{ color: '#fff' }}>
            <nav className={sidebar ? 'sidebar-menu active' : 'sidebar-menu'}>
                <ul className='sidebar-menu-items'>
                    <li className='sidebar-toggle'>
                        <Link to='#' className='menu-bars'>
                            { sidebar ?  <FaIcons.FaTimes onClick={showSidebar}/> : <FaIcons.FaBars onClick={showSidebar}/>}
                        </Link>
                    </li>
                    {SidebarData.map((barButton, index) => {
                        return (
                            <li key={index} className={barButton.className}>
                                <div>
                                <Link to={barButton.path}>
                                    {barButton.icon}
                                    { sidebar? <span>{barButton.title}</span> : null}
                                </Link>
                                </div>
                            </li>
                        );
                    })}
                </ul>
            </nav>
        </IconContext.Provider>
    )
}

export default Sidebar
