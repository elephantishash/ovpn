import React from 'react'
import { Link } from "react-router-dom"

function Header(){
  return (
    <div>
      <nav class="navbar navbar-expand-sm sticky-top bg-body-tertiary">
        <div class="container-fluid">
          <Link className="navbar-brand" to="/">Final VPN</Link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <div class="">
              <ul class="navbar-nav nav-underline me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                  <Link className="nav-link" to="/login">Login</Link>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </nav>
    </div>
  )
}

export default Header;
