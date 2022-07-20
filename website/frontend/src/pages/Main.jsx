import { SearchBar } from '../components';
export function Main() {
  return (
    <div className="flex justify-center">
      <div className="flex flex-col items-center w-screen gap-3 py-4 font-arvo container-lg">
        <h1 className="text-xl font-bold ">Find books similar to...</h1>
        <SearchBar />
      </div>
    </div>
  );
}
