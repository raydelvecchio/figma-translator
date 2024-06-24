// This code implements a waitlist signup page based on the provided design.
// It includes a header with navigation, a main section with the waitlist form,
// and a footer with social media links. The component uses React, Tailwind CSS,
// and react-icons for styling and functionality.

import React, { useState } from 'react';
import { FaFacebookF, FaLinkedinIn, FaYoutube, FaInstagram } from 'react-icons/fa';

const Header = () => (
  <header className="flex justify-between items-center p-4">
    <div className="flex space-x-4">
      <span>Page</span>
      <span>Page</span>
      <span>Page</span>
    </div>
  </header>
);

const WaitlistForm = () => {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Implement form submission logic
    console.log('Submitting email:', email);
  };

  return (
    <div className="text-center my-20">
      <h1 className="text-4xl font-bold mb-4">Waitlist title</h1>
      <p className="mb-6">Sign up for the waitlist for updates</p>
      <form onSubmit={handleSubmit} className="flex justify-center">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email@janesfakedomain.net"
          className="border rounded-l px-4 py-2 w-64"
          required
        />
        <button type="submit" className="bg-black text-white px-4 py-2 rounded-r">
          Submit
        </button>
      </form>
    </div>
  );
};

const Footer = () => (
  <footer className="fixed bottom-0 left-0 right-0 flex justify-between items-center p-4">
    <div>Site name</div>
    <div className="flex space-x-4">
      <FaFacebookF />
      <FaLinkedinIn />
      <FaYoutube />
      <FaInstagram />
    </div>
  </footer>
);

const WaitlistPage = () => (
  <div className="min-h-screen flex flex-col">
    <Header />
    <main className="flex-grow">
      <WaitlistForm />
    </main>
    <Footer />
  </div>
);

export default WaitlistPage;