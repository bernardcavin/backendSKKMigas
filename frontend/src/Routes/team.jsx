import React from 'react';
import { useLoaderData } from 'react-router-dom';

// Loader untuk Team
export const teamLoader = async () => {
  // Contoh: ambil data dari API atau database
  const team = await fetch('/api/teamData').then(res => res.json());
  return { team };
};

const Team = () => {
  // Ambil data dari loader
  const { team } = useLoaderData();

  return (
    <div>
      <h1>Meet the Team</h1>
      <ul>
        {team.map((member) => (
          <li key={member.id}>
            {member.name} - {member.role}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Team;
