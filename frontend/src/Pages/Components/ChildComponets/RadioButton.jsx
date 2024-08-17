import React from 'react';

function RadioButton({ label, nameLabel, title, onChange, checked }) {
  return (
    <div className="inline-flex items-center">
      <label className="relative flex items-center p-3 rounded-full cursor-pointer" htmlFor={label}>
        <input
          name={nameLabel}
          type="radio"
          onChange={onChange}
          checked={checked}
          className="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-full border border-blue-gray-200 text-blue-500 transition-all checked:border-gray-900 checked:before:bg-gray-900 hover:before:opacity-10"
          id={label}
          value={title} // Nilai yang akan dikirim ke parent
        />
        <span className="absolute text-blue-500 transition-opacity opacity-0 pointer-events-none top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 peer-checked:opacity-100">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" viewBox="0 0 16 16" fill="currentColor">
            <circle data-name="ellipse" cx="8" cy="8" r="8"></circle>
          </svg>
        </span>
      </label>
      <label className="mt-px font-light text-gray-700 cursor-pointer select-none" htmlFor={label}>
        {title}
      </label>
    </div>
  );
}

export default RadioButton;
