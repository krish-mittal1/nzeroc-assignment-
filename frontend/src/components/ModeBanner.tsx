export default function ModeBanner(){
    const dataSource = process.env.NEXT_PUBLIC_DATA_SOURCE;

    if(dataSource == "live"){
        return (
            <div className="w-full bg-green-100 text-green-800 text-sm text-center py-2 border-b border-green-300">
             🟢 Live data — connected to backend API
            </div>
        )
    }

    if (dataSource == "demo"){
        return (
            <div className="w-full bg-yellow-100 text-yellow-800 text-sm text-center py-2 border-b border-yellow-300">
        🟡 Demo mode — showing sample data, not live events
      </div>
        )
    }

    return (
        <div className="w-full bg-red-100 text-red-800 text-sm text-center py-2 border-b border-red-300">
      🔴 NEXT_PUBLIC_DATA_SOURCE is not set — data source unknown
    </div>
    )
}