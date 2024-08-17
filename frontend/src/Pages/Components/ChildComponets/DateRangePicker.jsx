import React, { useEffect } from 'react'
import { useState } from 'react'
import { Input } from '@material-tailwind/react';

const DateRangePicker = ({sendData}) => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    const handleStartDateChange = (e) => {
        setStartDate(e.target.value);
        // Reset endDate if it's before the selected startDate
        if (endDate && e.target.value > endDate) {
            setEndDate('');
        }
    };

    const handleEndDateChange = (e) => {
        setEndDate(e.target.value);
    };

    
    

    useEffect(() => {
        sendData(startDate, endDate);
    }, [startDate, endDate]);

    return (
        <div>
            <label className='font-bold '>
                Rencana Mulai Tajak
                <Input
                    type="date"
                    value={startDate}
                    onChange={handleStartDateChange}
                    
                />
            </label>
            <br />
            <label className='font-bold '>
                Rencana Selesai Operasi
                <Input
                    type="date"
                    value={endDate}
                    onChange={handleEndDateChange}
                    min={startDate} // Set minimum date to startDate
                />
            </label>
        </div>
    );
}

export default DateRangePicker