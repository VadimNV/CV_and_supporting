
def new_slide(ioW,figName,Cap,points):
    ioW.write(r'\begin{landscape}'+'\n')

    ioW.write(r'\begin{figure}[!htbp]'+'\n')
    ioW.write(r'	\centering'+'\n')
    ioW.write(r'	\inputpgf{\pathnPlan \pathFigs}{'+figName+'.pgf}'+'\n')
    ioW.write(r'	\caption{'+Cap+'}'+'\n')
    ioW.write(r'\end{figure}'+'\n')
    #
    if len(points)>0:
        ioW.write(r'\begin{itemize}'+'\n')
        for bulletPtStr in points:
            ioW.write(r'\item '+bulletPtStr+'\n')
        ioW.write(r'\end{itemize}'+'\n')
    #
    ioW.write(r'\end{landscape}'+'\n\n')

def new_statement(ioW,Cap):
    ioW.write(r'\begin{landscape}'+'\n')
    ioW.write(r'\centerline{\LARGE\textbf{'+Cap+'}}\n')
    #
    ioW.write(r'\end{landscape}'+'\n\n')
