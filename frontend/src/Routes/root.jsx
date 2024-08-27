import React from 'react';
import { json, Outlet, useLoaderData } from 'react-router-dom';

// Loader untuk Root
export const rootLoader = async () => {
    // Contoh: ambil data dari API atau database
    const data = {
        "message": "This is the root page data."
    }
    const Jsondata = json(data);
    console.log(Jsondata);
    
    return { Jsondata };
};

const Root = () => {
    // Ambil data dari loader
    const { data } = useLoaderData();

    return (
        <div>
            <h1>Welcome to the Root Page</h1>
            <p>Data from loader: {JSON.stringify(data)}</p>
            {/* Outlet digunakan untuk merender komponen anak rute */}
            <Outlet />
        </div>
    );
};

export default Root;
