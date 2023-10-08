import React from 'react'
import { Link } from "react-router-dom"

function LoginPage() {
  return (
    <div className="container">
  		<form>
  			<div className="border p-3 m-3 rounded rounded-3">
  				<div className="col-md-auto">
  					<h3 className="text-center">Login</h3>
  					<input type="username" placeholder="Username" className="form-control" name="username" />
  					<br />
  					<input type="password" placeholder="Password" className="form-control" name="password" />
  					<br />
  					<div className="row p-2">
  						<button className="submit btn btn-primary col m-1" type="submit">Login</button>
  						<button className="submit btn btn-secondary col disabled m-1" type="submit">Register</button>
  					</div>
  				</div>
        </div>
  		</form>
  	</div>
  )
}

export default LoginPage;
