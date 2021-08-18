import * as FaIcons from 'react-icons/fa';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import './Topbar.css';

function Topbar() {
    return (
        <div>
            <li className='topbar'>
                <Link to='/signin' className='topbar-item'>
                    <span>Sign In</span>
                </Link>
            </li>
        </div>
    )
}

export default Topbar
