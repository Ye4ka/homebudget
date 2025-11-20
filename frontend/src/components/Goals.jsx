const Goals = () => {
  return (
    <div className="flex flex-col gap-y-5">
        <h2 className="font-montserrat font-semibold text-2xl">Цели</h2>
        <div className="flex flex-col gap-y-7">
            <div>
                <div class="flex justify-between mb-1">
                    <span class="font-montserrat font-medium">Путешествие</span>
                    <span class="font-montserrat font-medium">45%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-3">
                    <div class="bg-blue-600 h-3 rounded-full" style={{width: '45%'}}></div>
                </div>
            </div>
            <div>
                <div class="flex justify-between mb-1">
                    <span class="font-montserrat font-medium">Xbox</span>
                    <span class="font-montserrat font-medium">65%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-3">
                    <div class="bg-green-600 h-3 rounded-full" style={{width: '65%'}}></div>
                </div>
            </div>
            <div>
                <div class="flex justify-between mb-1">
                    <span class="font-montserrat font-medium">Кисти</span>
                    <span class="font-montserrat font-medium">15%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-3">
                    <div class="bg-orange-600 h-3 rounded-full" style={{width: '15%'}}></div>
                </div>
            </div>
        </div>
    </div>
  );
};

export default Goals;